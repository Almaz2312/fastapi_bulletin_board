import factory

from app.models.user import User
from app.tests.base import AsyncSQLAlchemyBaseFactory


class UserFactory(AsyncSQLAlchemyBaseFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    hashed_password = factory.Faker("password")
    is_active = True
    full_name = factory.Faker("name")
    phone_number = factory.Faker("phone_number")
