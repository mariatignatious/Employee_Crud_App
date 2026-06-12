"""
Database engine and session factory (async).

Uses SQLAlchemy async engine backed by asyncpg so every DB call is
non-blocking and stays on the event-loop thread instead of occupying a
thread-pool worker.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from config import settings

# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/employee_db"

Base = declarative_base()
# class Base(DeclarativeBase):
#    """Base class for ORM mapped classes (entities)."""

# engine is the bridge between our application (python) and the database, it manages the connection pool and executes the SQL queries, while AsyncSession is the interface we use to interact with the database in an async way, it provides methods for querying and manipulating the data in the database
engine = create_async_engine(
    settings.database_url, echo=False, pool_size=10, max_overflow=20
)  # echo true to see the SQL queries in the console, pool_size and max_overflow to control the connection pool size
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False
)  # expire_on_commit false to prevent the session from expiring the objects after commit, so we can still access them after commit without refreshing them from the database


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """One AsyncSession per request; closed after the request."""
    async with AsyncSessionLocal() as session:
        yield session


# async def create_tables() -> None:
#     """Create tables for all ORM models that inherit from Base."""
#     import models.employee  # noqa: F401 — registers the mapper before create_all

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

