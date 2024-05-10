from datetime import datetime
from typing import List, Annotated, Sequence

from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, get_async_session
from models import User, Category, Task
from schemas import CreateUser, ReadUser, CreateTask, ReadCategory, ReadTask
from base_config import auth_backend, current_user
from manager import get_user_manager

app = FastAPI()


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
app.include_router(fastapi_users.get_auth_router(auth_backend),
                   prefix='/auth/jwt', tags=['auth'])
app.include_router(fastapi_users.get_register_router(ReadUser, CreateUser),
                   prefix='/auth', tags=['auth'])


@app.get('/')
async def hello():
    return {'hello': 'world'}


@app.post('/categories')
async def category(title: str, user: Annotated[User, Depends(current_user)],
        session: AsyncSession = Depends(get_async_session)):
    category = Category(title=title, owner=user.id)
    session.add(category)
    await session.commit()
    return {'status': 'success',
            'detail': f'Категория {title} добавлена'}


@app.post('/task')
async def create_task(task: CreateTask, user: Annotated[User, Depends(current_user)],
                      session: AsyncSession = Depends(get_async_session)):
    if task.status <= 0 or task.status >= 4:
        raise HTTPException(status_code=400, detail='bad status')
    if task.deadline.replace(tzinfo=None) < datetime.utcnow():
        raise HTTPException(status_code=400, detail='bad deadline')
    query = select(Category).where(Category.id == task.category and Category.owner == user.id)
    category = await session.scalar(query)
    if not category:
        raise HTTPException(status_code=400, detail='category not found')
    task = Task(title=task.title, description=task.description, owner=user.id, category=task.category,
                status=task.status, deadline=task.deadline.replace(tzinfo=None))
    session.add(task)
    await session.commit()
    return {'status': 200,
            'detail': f'Задача {task.title} добавлена'}


@app.get('/category')
async def get_category_list(user: Annotated[User, Depends(current_user)],
                            session: AsyncSession = Depends(get_async_session)) -> List[ReadCategory]:
    query = select(Category).where(Category.owner == user.id)
    categories = await session.scalars(query)
    return categories.all()


@app.get('/category/{pk}')
async def get_category(pk: int, user: Annotated[User, Depends(current_user)],
                       session: AsyncSession = Depends(get_async_session)) -> ReadCategory:
    query = select(Category).where(Category.owner == user.id and id == pk)
    category = await session.scalar(query)
    if not category:
        raise HTTPException(status_code=404, detail='Not Found')
    return category


@app.get('/task')
async def get_task_list(user: Annotated[User, Depends(current_user)],
                        session: AsyncSession = Depends(get_async_session)) -> List[ReadTask]:
    query = select(Task).where(Task.owner == user.id)
    tasks = await session.scalars(query)
    return tasks.all()


@app.get('/task/{pk}')
async def get_task(pk: int, user: Annotated[User, Depends(current_user)],
                   session: AsyncSession = Depends(get_async_session)) -> ReadTask:
    query = select(Task).where(Task.owner == user.id and Task.id == pk)
    task = await session.scalar(query)
    if not task:
        raise HTTPException(status_code=404, detail='Not Found')
    return task