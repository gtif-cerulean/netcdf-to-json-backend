from pydantic.networks import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_url: HttpUrl


# NOTE: need mypy ignore because we want some args to come from the env
settings = Settings()  # type: ignore
