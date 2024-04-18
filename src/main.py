from random import randint
from typing import Union, List

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CreateUser, ReadUser
from models import User
from database import engine

app = FastAPI(title="Трекер задач", description="API для приложения "
                                                "отлеживания задач")


@app.get('/')
async def hello():
    return {"Hello": "World"}


@app.get('/user')
async def get_all_users(offset: int, limit: int) -> List[ReadUser]:
    async with AsyncSession(engine) as session:
        stmt = select(User).offset(offset).limit(limit)
        print(stmt)
        users = await session.scalars(stmt)
        return users.all()


@app.post('/user')
async def add_user(user: CreateUser) -> ReadUser:
    stmt = User(name=user.name, fullname=user.fullname, nickname=user.nickname)
    async with AsyncSession(engine) as session:
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
    return stmt


@app.get('/user/{user_id}')
async def get_one_user(user_id:int) -> ReadUser:
    """Выдает информацию об одном пользователе"""
    async with AsyncSession(engine) as session:
        stmt = select(User).where(User.id==user_id)  # запрос
        user = await session.scalars(stmt)  # выполние запроса
        return user.first()


@app.delete('/user/{user_id}')
async def delete_user(user_id:int) -> dict:
    async with AsyncSession(engine) as session:
        stmt = select(User).where(User.id == user_id)  # запрос
        user = await session.scalars(stmt)  # выполние запроса
        await session.delete(user.first())
        await session.commit()
        return {'status': 'success',
                'detail': f'User{user_id} has been deleted'}


@app.patch('/user/{user_id}')
async def update_user(user_id: int, new_user: CreateUser) -> ReadUser:
    async with AsyncSession(engine) as session:
        stmt = select(User).where(User.id == user_id)  # запрос
        result = await session.scalars(stmt)  # выполние запроса
        user: User = result.first()
        user.name = new_user.name
        user.fullname = new_user.fullname
        user.nickname = new_user.nickname
        session.add(user)
        await session.commit()
        stmt = select(User).where(User.id == user_id)
        result = await session.scalars(stmt)
        return result.first()

