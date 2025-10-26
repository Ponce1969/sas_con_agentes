# backend/app/domain/models.py

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ----------------- MODELOS -----------------

class Role(Base, AsyncAttrs):
    __tablename__ = "roles"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), unique=True, nullable=False)
    description: Optional[str] = Column(String(255), nullable=True)

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"

class User(Base, AsyncAttrs):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(50), unique=True, nullable=False, index=True)
    email: str = Column(String(120), unique=True, nullable=False, index=True)
    hashed_password: str = Column(String(255), nullable=False)
    is_active: bool = Column(Boolean, default=True)
    is_superuser: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    role_id: Optional[int] = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

