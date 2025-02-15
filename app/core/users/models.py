from datetime import datetime

from sqlalchemy import INTEGER, TIMESTAMP, VARCHAR, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    email: Mapped[str] = mapped_column(VARCHAR(length=255), unique=True, nullable=True)
    username: Mapped[str] = mapped_column(VARCHAR(length=32), unique=True, index=True, nullable=False)
    first_name: Mapped[str | None] = mapped_column(VARCHAR(length=32), nullable=True)
    last_name: Mapped[str | None] = mapped_column(VARCHAR(length=32), nullable=True)
    ban_reason: Mapped[str | None] = mapped_column(String(length=1024), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now)
    password: Mapped[str] = mapped_column(String(length=32), nullable=False)
