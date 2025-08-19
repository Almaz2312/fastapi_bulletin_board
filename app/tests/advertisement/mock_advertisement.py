from typing import List

import factory
from factory import fuzzy
from factory.base import T
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.advertisement import Category, SubCategory, Advertisement
from app.models.base_class import Base
from app.tests.conftest import sessionmanager


class AsyncSQLAlchemyBaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "flush"

    @classmethod
    async def create_mock_data(cls, **kwargs):
        data = cls.build(**kwargs)
        async with sessionmanager.session() as session:
            session.add(data)
            await session.commit()
        return data

    @classmethod
    async def create_batch_mock_data(cls, size: int, **kwargs):
        objs = cls.build_batch(size=size, **kwargs)
        async with sessionmanager.session() as session:
            session.add_all(objs)
            await session.commit()
        return objs


class CategoryFactory(AsyncSQLAlchemyBaseFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")


class SubCategoryFactory(AsyncSQLAlchemyBaseFactory):
    class Meta:
        model = SubCategory

    name = factory.Faker("name")
    category = factory.SubFactory(CategoryFactory)
