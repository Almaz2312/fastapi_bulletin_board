import os
import sys
from typing import Generator, Any, AsyncGenerator

import httpx
import pytest_asyncio as pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.config.settings import settings
from app.db.session import DatabaseSessionManager, get_db_session
from app.api.base import api_router
from app.models.base_class import Base
from app.tests.utils import authentication_token_from_email

kwargs = {"echo": False, "pool_pre_ping": True, "pool_recycle": 3600}
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
sessionmanager = DatabaseSessionManager(DATABASE_URL, kwargs)


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


@pytest.fixture(scope="function")
async def app() -> Generator[FastAPI, Any, None]:
    async with sessionmanager.connect() as connect:
        await connect.run_sync(Base.metadata.create_all)
    _app = start_application()
    yield _app
    async with sessionmanager.connect() as connect:
        await connect.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def test_db_session() -> AsyncGenerator[async_sessionmaker, Any]:
    async with sessionmanager.session() as session:
        trans = await session.begin()
        try:
            yield session
        finally:
            await trans.rollback()


@pytest.fixture(scope="function")
async def client(app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, None]:
    async def _get_test_db_session():
        try:
            async with sessionmanager.session() as session:
                yield session
        finally:
            pass

    app.dependency_overrides[get_db_session] = _get_test_db_session
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="module")
async def normal_user_token_headers(client: httpx.AsyncClient, test_db_session: AsyncSession):
    return await authentication_token_from_email(client=client, email="TestUser@mail.com", db=test_db_session)
