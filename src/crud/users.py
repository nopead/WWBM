from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.auth import User as UserORM
from sqlalchemy import select, func


class UserService:

    @staticmethod
    async def is_exists(id: int, session: AsyncSession):

        result = await session.execute(select(func.count()).select_from(UserORM).filter(UserORM.id == id))
        count = result.scalar()

        if count > 0:
            return True

        return False
