import datetime

from pydantic import BaseModel


class ProxyDTO(BaseModel):
    id: int
    ip: str
    port: int
    username: str
    password: str
    proxy_type: str
    country: str
    created_on: datetime.datetime
    service_name: str
    job_names: list[str]
    active: bool

    class Config(object):
        orm_mode = True


class PostProxyDTO(BaseModel):
    ip: str
    port: int
    username: str
    password: str
    proxy_type: str
    country: str
    service_name: str
    job_names: list[str]
    active: bool


class PutProxyDTO(BaseModel):
    port: int
    username: str
    password: str
    job_names: list[str]
    active: bool


class ProxyGenerated(BaseModel):
    proxy_id: int
    ip: str
    port: int
    username: str
    password: str
