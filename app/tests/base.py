import factory

from app.tests.conftest import test_sessionmanager


class AsyncSQLAlchemyBaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "flush"

    @classmethod
    async def create_mock_data(cls, **kwargs):
        data = cls.build(**kwargs)
        async with test_sessionmanager.session() as session:
            session.add(data)
            await session.commit()
        return data

    @classmethod
    async def create_batch_mock_data(cls, size: int, **kwargs):
        objs = cls.build_batch(size=size, **kwargs)
        async with test_sessionmanager.session() as session:
            session.add_all(objs)
            await session.commit()
        return objs
