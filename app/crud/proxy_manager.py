from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.proxy import Proxy
from models.proxy_using_history import ProxyUsingHistory
from dtos.proxy import ProxyGenerated
from sqlalchemy import text
import random
import logging
from datetime import datetime

last_return_dt = []
all_proxies = []
was_inited = False


class ProxyManager:
    def __init__(self, db: AsyncSession, logger: logging.Logger = None):
        self.db = db
        self.logger = logger

    async def get_all_actives(
            self, page_limit: int = None, page_offset: int = None, job_name: str = None, proxy_type: str = None
    ):
        """
        Get all active proxies
        :param page_limit:
        :param page_offset:
        :param job_name:
        :param proxy_type:
        :return:
        """
        query = select(Proxy).where(Proxy.active == True)
        if job_name:
            query = query.where(text(f"proxy.job_names @> '[\"{job_name}\"]'"))
        if page_limit:
            query = query.limit(page_limit)
        if page_offset:
            query = query.offset(page_offset)
        if proxy_type:
            query = query.where(Proxy.proxy_type == proxy_type)
        proxies = await self.db.execute(
            query
        )
        proxies = proxies.scalars().all()
        return proxies

    async def update_all_proxies(self):
        """
        Update all proxies
        :return:
        """
        global all_proxies
        all_proxies = await self.db.execute(
            select(Proxy).where(Proxy.active == True)
        )
        all_proxies = all_proxies.scalars().all()

    async def get_by_id(self, proxy_id: int):
        """
        Get a proxy by id
        :param proxy_id:
        :return:
        """
        proxy = await self.db.get(Proxy, proxy_id)
        return proxy

    async def post(
            self,
            ip: str,
            port: int,
            username: str,
            password: str,
            proxy_type: str,
            country: str,
            service_name: str,
            job_names: list[str],
            active: bool
    ):
        """
        Add a new proxy to
        :param ip:
        :param port:
        :param username:
        :param password:
        :param proxy_type:
        :param country:
        :param service_name:
        :param job_names:
        :param active:
        :return:
        """
        proxy = Proxy(
            ip=ip, country=country, service_name=service_name, job_names=job_names, active=active, port=port,
            username=username, password=password, proxy_type=proxy_type
        )
        self.db.add(proxy)
        await self.db.commit()
        await self.db.refresh(proxy)
        return proxy

    async def edit_proxy(
            self,
            proxy_id: int,
            job_names: list[str] = None,
            active: bool = None,
            username: str = None,
            password: str = None,
            port: int = None,
            proxy_type: str = None
    ):
        """
        Edit a proxy
        :param proxy_id:
        :param job_names:
        :param active:
        :param username:
        :param password:
        :param port:
        :param proxy_type:
        :return:
        """
        proxy = await self.get_by_id(proxy_id)
        if proxy is None or (job_names is None and active is None) or proxy.active is False:
            return None
        if job_names is not None:
            proxy.job_names = job_names
        if active is not None:
            proxy.active = active
        if username is not None:
            proxy.username = username
        if password is not None:
            proxy.password = password
        if port is not None:
            proxy.port = port
        if proxy_type is not None:
            proxy.proxy_type = proxy_type
        await self.db.commit()
        await self.db.refresh(proxy)
        return proxy

    async def generate_proxy(self, job_name: str, count: int, proxy_type: str) -> list[ProxyGenerated]:
        """
        Generate a proxy
        :param job_name:
        :param count:
        :param proxy_type:
        :return:
        """
        global was_inited
        global all_proxies
        global last_return_dt
        if not was_inited:
            await self.update_all_proxies()
            was_inited = True
        proxies = list(filter(lambda x: job_name in x.job_names and x.proxy_type == proxy_type, all_proxies))
        proxies_ids = list(map(lambda x: x.id, proxies))
        proxies_were = list(filter(lambda x: x["job_name"] == job_name and
                                             x["proxy_id"] in proxies_ids and
                                             x["proxy_type"] == proxy_type, last_return_dt))
        proxies_were_id = list(map(lambda x: x["proxy_id"], proxies_were))
        proxies_were_not = list(filter(lambda x: x not in proxies_were_id, proxies_ids))
        proxies_not_were_to_generate = min(count, len(proxies_were_not))
        proxy_ids_to_out = []
        if proxies_not_were_to_generate > 0:
            proxies = random.sample(proxies_were_not, proxies_not_were_to_generate)
            proxy_ids_to_out.extend(proxies)
        if len(proxy_ids_to_out) < count:
            proxies_were_to_generate = count - len(proxy_ids_to_out)
            proxies = list(map(lambda x: x["proxy_id"], sorted(proxies_were, key=lambda x: x["dt"], reverse=False)[:proxies_were_to_generate]))
            proxy_ids_to_out.extend(proxies)

        proxies_to_out = list(filter(lambda x: x.id in proxy_ids_to_out, all_proxies))

        generated_proxies = []
        for proxy in proxies_to_out:
            proxy_info = ProxyGenerated(
                proxy_id=proxy.id,
                ip=proxy.ip,
                port=proxy.port,
                username=proxy.username,
                password=proxy.password
            )
            generated_proxies.append(proxy_info)
            last_return_dt = list(filter(lambda x: x["proxy_id"] != proxy.id and x["job_name"] == job_name, last_return_dt))
            last_return_dt.append({
                "dt": datetime.now(), "job_name": job_name, "proxy_id": proxy.id, "proxy_type": proxy_type
            })
        return generated_proxies

    async def save_history(self, job_name: str, proxy_infos: list[ProxyGenerated]):
        """
        Save a history of using proxy
        :param job_name:
        :param proxy_infos:
        :return:
        """
        for proxy_info in proxy_infos:
            history = ProxyUsingHistory(
                proxy_id=proxy_info.proxy_id,
                job_name=job_name
            )
            self.db.add(history)
        await self.db.commit()
