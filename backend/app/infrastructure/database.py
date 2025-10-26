# backend/app/infrastructure/database.py

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ----------------- CONFIG -----------------
DB_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# ----------------- ENGINE -----------------
engine = create_async_engine(
    DB_URL,
    echo=False,  # Cambiar a True para debug SQL
    future=True,
)

# ----------------- SESSION -----------------
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# ----------------- BASE -----------------
Base = declarative_base()

# ----------------- DEPENDENCY -----------------
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to provide async DB session.
    Usage: `async with get_async_session() as session: ...`
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# ----------------- UTILITY -----------------
async def init_db():
    """
    Create all tables in the database. 
    Call this at startup or in a migration script.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ----------------- EXAMPLE USAGE -----------------
# from fastapi import Depends
# async def some_service(session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(select(User))
#     users = result.scalars().all()

