import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail
            },
            "status": "Error"
        },
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "message": "\n".join(
                    f"{'.'.join(error['loc'][1:] or error['loc'][:1])}: {error['msg']}"
                    for error in exc.errors()
                ),
            },
            "status": "Error",
        },
    )


async def base_exception_handler(request: Request, err):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "message": f"{err}",
                "method": f"{request.method}: {request.url}"
            },
            "status": "Error"
        },
    )
