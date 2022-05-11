import os
from logging import config as logging_config

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    RUN_CLEAN_UP: bool = ENVIRONMENT == "production" or bool(os.getenv("RUN_CLEAN_UP", False))

    BUCKET_NAME: str = os.getenv("BUCKET_NAME", "")

    RUNNING_MODE: str = os.getenv("RUNNING_MODE", "foreground")
    SECRET_PASSPHRASE: str = os.getenv("SECRET_PASSPHRASE", "")

    logging_config.fileConfig(f"logging.{ENVIRONMENT}.conf", disable_existing_loggers=False)


app_settings: Settings = Settings()
