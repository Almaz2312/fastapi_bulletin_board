from typing import Optional

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy import select
from starlette.authentication import AuthenticationBackend, AuthCredentials, AuthenticationError, UnauthenticatedUser, BaseUser
from starlette.requests import HTTPConnection

from app.config.settings import settings
from app.db.session import sessionmanager
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login/", auto_error=False)


class BaseAuthentication(AuthenticationBackend):
    def __init__(self, exception: Optional[HTTPException] = None):
        if exception is not None:
            exception = self.default_exception
        self.exception = exception

    async def authenticate(
            self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, BaseUser] | tuple[AuthCredentials, UnauthenticatedUser]:
        token = await oauth2_scheme(conn)
        # return anonymous user if token was not provided
        if not token:
            return AuthCredentials(["anonymous user"]), UnauthenticatedUser()

        try:
            sub = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]).get("sub")
            if not sub:
                raise await self.credentials_exception()
        except JWTError as e:
            raise await self.credentials_exception(str(e))

        async with sessionmanager.session() as session:
            query = select(User).where(User.username == sub)
            query_result = await session.execute(query)
            user = query_result.scalar_one_or_none()
            if not user:
                raise await self.credentials_exception()
            user.is_authenticated = True

        return AuthCredentials("authenticated"), user

    @staticmethod
    async def credentials_exception(detail="Could not validate credentials."):
        cred_error = AuthenticationError(detail)
        return cred_error
