from typing import Dict

from pydantic import BaseSettings


class Settings(BaseSettings):

    database_url: str = ...
    logging_config: str = "./logging.toml"


settings = Settings()
