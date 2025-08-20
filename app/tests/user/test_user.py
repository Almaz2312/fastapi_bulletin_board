import faker
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import ProfileSchema
from app.tests.user.mock_user import UserFactory

pytest_plugin = ["pytest_asyncio"]
pytestmark = pytest.mark.asyncio


class TestUser:
    base_url = "/api/v1/users/"

    async def test_create_user(self, client):
        password = faker.Faker().password()
        user_data = {
            "username": faker.Faker().user_name(),
            "email": faker.Faker().email(),
            "password": password,
            "confirm_password": password,
            "full_name": faker.Faker().name(),
            "phone_number": faker.Faker().phone_number(),
        }

        response = await client.post(self.base_url + "register-user", json=user_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("username") == user_data.get("username")

    async def test_get_users(self, client):
        await UserFactory.create_batch_mock_data(size=5)

        response = await client.get(self.base_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 5

    async def test_get_profile(
        self, client, normal_user_token_headers, test_db_session: AsyncSession
    ):

        # + 1 user since normal_user_token_headers creates one
        await UserFactory.create_batch_mock_data(size=5)
        user_repo = UserRepository(test_db_session)
        current_user = await user_repo.get_user_by_field(
            User.username, "TestUser@mail.com"
        )

        response = await client.get(
            self.base_url + f"profile", headers=normal_user_token_headers
        )
        cur = ProfileSchema.model_validate(current_user).model_dump()

        assert response.status_code == status.HTTP_200_OK
        assert cur == response.json()
