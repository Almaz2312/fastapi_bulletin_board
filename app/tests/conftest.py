from typing import Any, AsyncGenerator, Generator

import httpx
import pytest_asyncio as pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import DatabaseSessionManager, get_db_session
from app.models.base_class import Base
from app.tests.utils import authentication_token_from_email

kwargs = {"echo": False, "pool_pre_ping": True, "pool_recycle": 3600}
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_sessionmanager = DatabaseSessionManager(DATABASE_URL, kwargs)


@pytest.fixture(scope="function")
async def app() -> AsyncGenerator[FastAPI, None]:
    import app.db.session

    app.db.session.sessionmanager = test_sessionmanager

    async with test_sessionmanager.connect() as connect:
        await connect.run_sync(Base.metadata.create_all)

    from app.server import start_application

    _app = start_application()
    yield _app
    async with test_sessionmanager.connect() as connect:
        await connect.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def test_db_session() -> AsyncGenerator[AsyncSession, Any]:
    async with test_sessionmanager.session() as session:
        yield session


@pytest.fixture(scope="function")
async def client(app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, None]:
    async def _get_test_db_session():
        try:
            async with test_sessionmanager.session() as session:
                yield session
        finally:
            pass

    app.dependency_overrides[get_db_session] = _get_test_db_session
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def normal_user_token_headers(
    client: httpx.AsyncClient, test_db_session: AsyncSession
):
    return await authentication_token_from_email(
        client=client, email="TestUser@mail.com", db=test_db_session
    )
