from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings


class LoginRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            claims=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
