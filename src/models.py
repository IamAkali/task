from typing import Optional
from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)


class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    owner: Mapped[int] = mapped_column(ForeignKey('user.id'))


class Task(Base):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    owner: Mapped[int] = mapped_column(ForeignKey('user.id'))
    category: Mapped[int] = mapped_column(ForeignKey('category.id'))
    status: Mapped[int] = mapped_column(default=0)
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    deadline: Mapped[datetime] = mapped_column(nullable=True)





