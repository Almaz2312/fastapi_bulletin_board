from typing import Any

from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from starlette import status

from app.config.settings import settings
from app.generics.security import Hasher
from app.models.user import User
from app.schemas.user import UserRegistrationSchema


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_user_by_field(self, field: InstrumentedAttribute, value: Any) -> User:
        query = select(User).where(field == value)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, data: UserRegistrationSchema):
        user_data = data.model_dump()
        password = user_data.pop("password")
        confirm_password = user_data.pop("confirm_password")
        if password != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Passwords do not match"},
            )
        user_data.update({"hashed_password": Hasher.get_password_hash(password)})

        new_user = User(**user_data)
        self.db.add(new_user)
        return new_user

    async def get_users(self):
        query = select(User)
        result = await self.db.execute(query)
        return result.scalars()

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user_by_field(User.username, username)
        if not user:
            return False

        if not Hasher.verify_password(password, user.hashed_password):
            return False

        return user

    async def verify_token(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

        try:
            decoded_token = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = decoded_token.get("sub")

            if not username:
                raise credentials_exception

        except JWTError as e:
            credentials_exception.detail = str(e)
            raise credentials_exception

        user = self.get_user_by_field(User.username, username)
        if not user:
            raise credentials_exception
        return user
