from typing import Dict

from pydantic import BaseSettings


class Settings(BaseSettings):

    database_url: str = ""
    db_user: str = ...
    db_password: str = ...
    db_host: str = ...
    db_name: str = ...


settings = Settings()
