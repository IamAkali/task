from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from config import DB_NAME, DB_PORT, DB_USER, DB_HOST, DB_PASS

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL, echo=True)