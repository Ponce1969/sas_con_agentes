# backend/app/infrastructure/repositories.py

from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base
from sqlalchemy import update, delete
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()
T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    """
    Repositorio genérico para modelos SQLAlchemy async.
    Maneja operaciones CRUD básicas.
    """

    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self) -> List[T]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.commit()

    async def bulk_add(self, objs: List[T]) -> List[T]:
        self.session.add_all(objs)
        await self.session.commit()
        for obj in objs:
            await self.session.refresh(obj)
        return objs

# ----------------- EJEMPLO DE USO -----------------
# from domain.models import User
# from infrastructure.database import async_session
# async with async_session() as session:
#     user_repo = BaseRepository(User, session)
#     user = await user_repo.add(User(name="Gonzalo"))
#     print(user.id)

