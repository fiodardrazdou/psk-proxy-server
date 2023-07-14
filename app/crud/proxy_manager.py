from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.proxy import Proxy
from models.proxy_using_history import ProxyUsingHistory
from dtos.proxy import ProxyGenerated
import random
import logging


class ProxyManager:
    def __init__(self, db: AsyncSession, logger: logging.Logger = None):
        self.db = db
        self.logger = logger
        self.history_of_generation = []

    async def get_all_actives(self, page_limit: int = None, page_offset: int = None):
        """
        Get all active proxies
        :param page_limit:
        :param page_offset:
        :return:
        """
        query = select(Proxy).where(Proxy.active == True)
        if page_limit:
            query = query.limit(page_limit)
        if page_offset:
            query = query.offset(page_offset)
        proxies = await self.db.execute(
            query
        )
        proxies = proxies.scalars().all()
        return proxies

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
    ):
        """
        Edit a proxy
        :param proxy_id:
        :param job_names:
        :param active:
        :param username:
        :param password:
        :param port:
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
        await self.db.commit()
        await self.db.refresh(proxy)
        return proxy

    async def generate_proxy(self, job_name: str, count: int) -> list[ProxyGenerated]:
        """
        Generate a proxy
        :param job_name:
        :param count:
        :return:
        """
        proxies = await self.get_all_actives()
        if len(proxies) < count:
            self.logger.info(f"Proxy is not enough for {job_name}")
        proxies = random.sample(proxies, count)
        generated_proxies = []
        for proxy in proxies:
            proxy_info = ProxyGenerated(
                proxy_id=proxy.id,
                ip=proxy.ip,
                port=proxy.port,
                username=proxy.username,
                password=proxy.password
            )
            generated_proxies.append(proxy_info)
            self.history_of_generation.append(proxy_info)
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

    async def delete_proxy(self, proxy_id: int):
        """
        Delete a proxy
        :param proxy_id:
        :return:
        """
        proxy = await self.get_by_id(proxy_id)
        if proxy is None:
            return None
        await self.db.delete(proxy)
        await self.db.commit()
        return proxy
