import os

import factory
from dotenv import load_dotenv

from app.infra.database.db_adapter import Database
from settings.config import load_app_settings, AppSettings


def load_settings() -> AppSettings:
    is_local_test = os.getenv("LOCALTEST", "False").lower() in ("true", "1", "t")
    test_environment_path = "settings/environments/.env.local.runtests" if is_local_test else None
    load_dotenv(test_environment_path, override=is_local_test)
    return load_app_settings()


database = Database(load_settings())


class BaseModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = database.get_sync_db_session()