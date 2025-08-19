import time

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.user import User
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.schemas.user import UserRegistrationSchema


async def user_authentication_headers(client: AsyncClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = await client.post("api/v1/auth/login", json=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def authentication_token_from_email(client: AsyncClient, email: str, db: AsyncSession):
    password = "random-passW0rd"
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_field(User.email, email)
    if not user:
        user_in_create = UserRegistrationSchema(
            username=email, email=email,
            password=password, confirm_password=password,
            full_name="Test test test"
        )
        user_service = UserService(db)
        user = await user_service.register_user(user_in_create)
    access_token = await user_authentication_headers(client=client, email=email, password=password)
    return access_token
