import logging
from typing import List

from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dtos.generic import SuccessResponse

from crud.proxy_manager import ProxyManager
from database import get_db
from dtos.proxy import ProxyDTO, PostProxyDTO, PutProxyDTO, ProxyGenerated

router = APIRouter()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@router.get("/proxies", response_model=SuccessResponse[List[ProxyDTO]])
async def get_all_proxies(
        page_offset: int = Query(0, ge=0),
        page_limit: int = Query(100, ge=1),
        db: AsyncSession = Depends(get_db)
):
    proxy_values = await ProxyManager(db, logger).get_all_actives(page_limit=page_limit, page_offset=page_offset)
    return SuccessResponse(data=proxy_values)


@router.get("/proxy/{proxy_id}", response_model=SuccessResponse[ProxyDTO])
async def get_one_proxy(proxy_id: int, db: AsyncSession = Depends(get_db)):
    proxy = await ProxyManager(db, logger).get_by_id(proxy_id)

    if not proxy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return SuccessResponse(data=proxy)


@router.post("/proxy", response_model=SuccessResponse[ProxyDTO])
async def create_proxy(proxy: PostProxyDTO, db: AsyncSession = Depends(get_db)):
    proxy_value = await ProxyManager(db, logger).post(
        proxy.ip, proxy.port, proxy.username, proxy.password, proxy.proxy_type, proxy.country,
        proxy.service_name, proxy.job_names, proxy.active
    )
    print(proxy_value)
    return SuccessResponse(data=proxy_value)


@router.put("/proxy/{proxy_id}", response_model=SuccessResponse[ProxyDTO])
async def update_metric(proxy_id: int, proxy: PutProxyDTO, db: AsyncSession = Depends(get_db)):
    metric_value = await ProxyManager(db, logger).edit_proxy(
        proxy_id,
        port=proxy.port,
        username=proxy.username,
        password=proxy.password,
        job_names=proxy.job_names,
        active=proxy.active
    )

    return SuccessResponse(data=metric_value)


@router.get("/proxy/generate/{count}", response_model=SuccessResponse[ProxyGenerated])
async def generate_proxies(count: int, job_name: str, db: AsyncSession = Depends(get_db)):
    proxy = await ProxyManager(db, logger).generate_proxy(job_name, count)

    return SuccessResponse(data=proxy)


@router.delete("/proxy/{proxy_id}", response_model=SuccessResponse[ProxyDTO])
async def delete_proxy(proxy_id: int, db: AsyncSession = Depends(get_db)):
    proxy = await ProxyManager(db, logger).delete_proxy(proxy_id)

    return SuccessResponse(data=proxy)
