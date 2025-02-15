from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base for all models.

    It has some type definitions to
    enhance autocompletion.
    """

    @classmethod
    def get_real_column_name(cls, attr_name: str) -> str:
        return getattr(inspect(cls).c, attr_name).name

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        try:
            return f"{self.__class__.__name__}(id={self.id})"  # type: ignore[attr-defined]
        except AttributeError:
            return super().__repr__()
