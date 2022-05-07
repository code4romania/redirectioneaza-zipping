import os
from logging import config

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    BUCKET_NAME: str = os.getenv("BUCKET_NAME", "")

    config.fileConfig(f"logging.{ENVIRONMENT}.conf", disable_existing_loggers=False)


app_settings: Settings = Settings()
