# backend/app/infrastructure/database.py

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.domain.models import Base

logger = logging.getLogger(__name__)

# ----------------- ENGINE -----------------
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# ----------------- SESSION -----------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# ----------------- DEPENDENCY -----------------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency para obtener sesión de DB.
    Uso: session: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ----------------- INIT DB -----------------
async def init_db() -> None:
    """Crear todas las tablas en la base de datos."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Base de datos inicializada")


async def create_default_roles(session: AsyncSession) -> None:
    """Crear roles por defecto si no existen."""
    from sqlalchemy import select

    from app.domain.models import Role

    # Verificar si ya existen roles
    result = await session.execute(select(Role))
    if result.scalars().first():
        return

    # Crear roles por defecto
    roles = [
        Role(id=1, name="free", description="Plan gratuito", max_analyses_per_day=5),
        Role(id=2, name="pro", description="Plan profesional", max_analyses_per_day=100),
        Role(id=3, name="custom", description="Plan con API key propia", max_analyses_per_day=9999),
        Role(id=4, name="admin", description="Administrador", max_analyses_per_day=9999),
    ]

    for role in roles:
        session.add(role)

    await session.commit()
    logger.info("✅ Roles por defecto creados")

