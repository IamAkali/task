from typing import List

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine
from models import User
from schemas import CreateUser, ReadUser
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



