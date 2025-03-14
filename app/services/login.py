from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config.settings import settings
from app.repositories.login import LoginRepository
from app.repositories.user import UserRepository
from app.schemas.login import LoginSchema, TokenSchema, SimpleTokenSchema


class LoginService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.repository = LoginRepository(db_session)
        self.user_repository = UserRepository(db_session)

    async def login(self, data: LoginSchema) -> TokenSchema:
        user = await self.user_repository.authenticate_user(data.username, data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        new_refresh_token = await self.repository.create_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_HOURS)
        )

        new_access_token = await self.repository.create_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return TokenSchema(access_token=new_access_token, refresh_token=new_refresh_token)

    async def refresh_token(self, token: SimpleTokenSchema) -> SimpleTokenSchema:
        user = await self.user_repository.verify_token(token.token)
        token = await self.repository.create_token({"sub": user.username})
        return SimpleTokenSchema(token=token)

    async def verify_token(self, token: SimpleTokenSchema) -> bool:
        user = await self.user_repository.verify_token(token.token)
        return user
