import factory

from app.infra.database.db_adapter import Database
from settings.config import load_app_settings


class RaiseError(Exception):
    """Custom exception to raise from mocked (override) dependencies."""

    def __init__(self, message: str | None = None):
        self._message = message or "raise error"

    def __str__(self) -> str:
        return str(self._message)


database = Database(load_app_settings())


class BaseModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = database.get_sync_db_session()
