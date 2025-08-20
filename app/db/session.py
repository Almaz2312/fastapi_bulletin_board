import contextlib
from typing import Any, AsyncGenerator, AsyncIterator, Dict

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
kwargs = {
    "echo": settings.ECHO,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "max_overflow": 100,
}


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: Dict[str, Any]):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine, expire_on_commit=False
        )
        self._exception = Exception("DatabaseSessionManager is not initialized")

    async def close(self):
        if self._engine is None:
            raise self._exception

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncGenerator[AsyncConnection, None]:
        if self._engine is None:
            raise self._exception

        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception:
                await conn.close()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise self._exception

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(SQLALCHEMY_DATABASE_URL, kwargs)


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session
