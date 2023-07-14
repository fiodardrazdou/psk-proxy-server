from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware


from config import settings
# from .logging import load_config, server_access_middleware
from routers import proxy
from exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    base_exception_handler
)

# load_config(settings.logging_config)

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(BaseHTTPMiddleware, dispatch=server_access_middleware)

app.include_router(proxy.router, tags=["proxy"])

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)
app.add_exception_handler(
    RequestValidationError,
    request_validation_exception_handler,
)
app.add_exception_handler(
    Exception,
    base_exception_handler,
)


@app.get("/")
async def root():
    return {"message": "Вітаю ў АПІ!"}
