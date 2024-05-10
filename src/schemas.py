from pydantic import BaseModel
from typing import Optional
from fastapi_users import schemas
from datetime import datetime


class CreateUser(schemas.BaseUserCreate):
    password: str
    email: str
    username:str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    fullname: str


class ReadUser(schemas.BaseUser[int]):
    id: int
    fullname: str
    email: str
    username: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    registered_at: datetime


class CreateTask(BaseModel):
    title: str
    description: str
    category: int
    status: int
    deadline: datetime


class ReadCategory(BaseModel):
    id: int
    title: str
    owner: int


class ReadTask(BaseModel):
    id: int
    title: str
    description: str
    owner: int
    category: int
    status: int
    created: datetime
    deadline: datetime