import os
from logging import config

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    BUCKET_NAME: str = os.getenv("BUCKET_NAME", "")
    RUNNING_MODE: str = os.getenv("RUNNING_MODE", "foreground")

    config.fileConfig(f"logging.{ENVIRONMENT}.conf", disable_existing_loggers=False)


app_settings: Settings = Settings()
