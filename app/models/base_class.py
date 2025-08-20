import re
from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    id: Any

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z][a-z])", "_", cls.__name__).lower()
