import os
from functools import lru_cache, cached_property

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

from app.core.constants import StageEnum, LogLevelEnum


class BaseAppSettings(BaseSettings):
    STAGE: StageEnum
    LOG_LEVEL: LogLevelEnum
    ENABLE_JSON_LOGS: bool
    LOCALTEST: bool
    model_config = SettingsConfigDict(env_file="settings/environments/.env", extra="ignore")


class DataBaseSettings(BaseSettings):
    POSTGRES_DB_PORT: int = 5433
    POSTGRES_DB: str = "example_database"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "postgrespwd"
    DB_ECHO: bool
    DB_HOST: str


class UsersSettings(BaseSettings):
    USER_KEY_HEADER: SecretStr


class AppSettings(BaseAppSettings, DataBaseSettings, UsersSettings, BaseSettings):
    DEBUG: bool
    APP_HOST: str
    APP_PORT: int

    @cached_property
    def async_db_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            database=self.POSTGRES_DB,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST,
            port=self.POSTGRES_DB_PORT,
        )

    @property
    def sync_db_url(self) -> URL:
        return URL.create(
            drivername="postgresql",
            database=self.POSTGRES_DB,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST,
            port=self.POSTGRES_DB_PORT,
        )


    model_config = SettingsConfigDict(case_sensitive=True)


@lru_cache(maxsize=None)  # noqa: UP033
def load_app_settings() -> AppSettings:
    is_local_test = os.getenv("LOCALTEST", "False").lower() in ("true", "1", "t") or BaseAppSettings
    app_env = StageEnum.runtests if is_local_test else BaseAppSettings().STAGE
    environment_path = "settings/environments/.env"
    if app_env is StageEnum.runtests and is_local_test:
        environment_path = "settings/environments/.env.local.runtests"
    load_dotenv(environment_path, override=is_local_test)
    return AppSettings()