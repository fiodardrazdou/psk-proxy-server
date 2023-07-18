import requests
from app.config import settings
from sqlalchemy import create_engine


class AutomationClient:

    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()

    def post_proxy(self, proxy: dict):
        return self.session.post(f"{self.url}/proxy", json=proxy)

    def get_proxy(self, proxy_id: int):
        return self.session.get(f"{self.url}/proxy/{proxy_id}")

    def edit_proxy(self, proxy_id: int, proxy: dict):
        return self.session.put(f"{self.url}/proxy/{proxy_id}", json=proxy)

    def delete_proxy(self, proxy_id: int):
        return self.session.delete(f"{self.url}/proxy/{proxy_id}")

    def get_proxies(
            self, page_offset: int = None, page_limit: int = None, job_name: str = None
    ):
        return self.session.get(
            f"{self.url}/proxies",
            params={"page_offset": page_offset, "page_limit": page_limit, "job_name": job_name}
        )

    def get_generate(self, count: int, job_name: str = None, proxy_type: str = None):
        return self.session.get(f"{self.url}/proxy/generate/{count}", params={"job_name": job_name,
                                                                              "proxy_type": proxy_type})
