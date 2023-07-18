from pydantic import BaseSettings


class TestSettings(BaseSettings):

    server_to_test_url: str = ""


settings = TestSettings()
