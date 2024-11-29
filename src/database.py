from curses.ascii import BEL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv

import os

from models import Base

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    _engine = create_async_engine(DATABASE_URL, echo=True)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await _engine.dispose()
