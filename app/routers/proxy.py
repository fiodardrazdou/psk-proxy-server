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
        job_name: str,
        proxy_type: str,
        page_offset: int = Query(0, ge=0),
        page_limit: int = Query(100, ge=1),
        db: AsyncSession = Depends(get_db)
):
    proxy_values = await ProxyManager(db, logger).get_all_actives(
        page_limit=page_limit, page_offset=page_offset, job_name=job_name, proxy_type=proxy_type
    )
    return SuccessResponse(data=proxy_values)


@router.get("/proxy/{proxy_id}", response_model=SuccessResponse[ProxyDTO])
async def get_one_proxy(proxy_id: int, db: AsyncSession = Depends(get_db)):
    proxy = await ProxyManager(db, logger).get_by_id(proxy_id)

    if not proxy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return SuccessResponse(data=proxy)


@router.post("/proxy", response_model=SuccessResponse[ProxyDTO])
async def create_proxy(proxy: PostProxyDTO, db: AsyncSession = Depends(get_db)):
    proxy_manager = ProxyManager(db, logger)
    proxy_value = await proxy_manager.post(
        proxy.ip, proxy.port, proxy.username, proxy.password, proxy.proxy_type, proxy.country,
        proxy.service_name, proxy.job_names, proxy.active
    )
    await proxy_manager.update_all_proxies()

    print(proxy_value)
    return SuccessResponse(data=proxy_value)


@router.put("/proxy/{proxy_id}", response_model=SuccessResponse[ProxyDTO])
async def update_metric(proxy_id: int, proxy: PutProxyDTO, db: AsyncSession = Depends(get_db)):
    proxy_manager = ProxyManager(db, logger)
    metric_value = await proxy_manager.edit_proxy(
        proxy_id,
        port=proxy.port,
        username=proxy.username,
        password=proxy.password,
        job_names=proxy.job_names,
        active=proxy.active,
        proxy_type=proxy.proxy_type,
    )
    await proxy_manager.update_all_proxies()

    return SuccessResponse(data=metric_value)


@router.get("/proxy/generate/{count}", response_model=SuccessResponse[List[ProxyGenerated]])
async def generate_proxies(count: int, proxy_type: str, job_name: str, db: AsyncSession = Depends(get_db)):
    proxy_manager = ProxyManager(db, logger)
    proxies = await proxy_manager.generate_proxy(job_name, count, proxy_type=proxy_type)
    await proxy_manager.save_history(job_name, proxies)

    return SuccessResponse(data=proxies)

