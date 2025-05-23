import re
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import DeclarativeBase


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z][a-z])', '_', cls.__name__).lower()
