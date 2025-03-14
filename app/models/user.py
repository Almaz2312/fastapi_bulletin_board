from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_class import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    full_name: Mapped[str] = mapped_column(nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=True, index=True, default=None)
