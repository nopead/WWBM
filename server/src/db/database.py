from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import DSN
from typing import Annotated
from fastapi import Depends

engine = create_async_engine(DSN, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


db_session_dependency = Annotated[AsyncSession, Depends(get_session)]
