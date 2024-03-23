from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.db.settings_db import postgres_settings

DATABASE_URL = postgres_settings.get_sqlalchemy_dsn()


engine = create_async_engine(DATABASE_URL, echo=True)

async_session_factory = async_sessionmaker(
    engine, autocommit=False, autoflush=False, expire_on_commit=False
)


@asynccontextmanager
async def get_db_ses():
    try:
        async_session = async_session_factory()
        async with async_session as session:
            yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_db_session():
    async with get_db_ses() as session:
        yield session
