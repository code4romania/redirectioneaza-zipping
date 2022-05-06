import os
from logging import config

from pydantic import BaseSettings


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "production")
    config.fileConfig(f"logging.{environment}.conf", disable_existing_loggers=False)


app_settings: Settings = Settings()
