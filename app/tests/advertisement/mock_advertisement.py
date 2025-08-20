import factory

from app.models.advertisement import Advertisement, Category, SubCategory
from app.tests.base import AsyncSQLAlchemyBaseFactory
from app.tests.user.mock_user import UserFactory


class CategoryFactory(AsyncSQLAlchemyBaseFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")


class SubCategoryFactory(AsyncSQLAlchemyBaseFactory):
    class Meta:
        model = SubCategory

    name = factory.Faker("name")
    category = factory.SubFactory(CategoryFactory)


class AdvertisementFactory(AsyncSQLAlchemyBaseFactory):
    class Meta:
        model = Advertisement

    user = factory.SubFactory(UserFactory)
    sub_category = factory.SubFactory(SubCategoryFactory)
    location = factory.Faker("address")
    price = factory.Faker("random_int")
    active = factory.Faker("boolean")
    negotiable = factory.Faker("boolean")
    description = factory.Faker("text")
    contact_email = factory.Faker("email")
    contact_phone = factory.Faker("phone_number")
    views = 0
