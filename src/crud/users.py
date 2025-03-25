from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.auth import User as UserORM
from sqlalchemy import select, func
from src.schemas.auth import User


class UserService:

    @staticmethod
    async def is_exists(
            id: int,
            session: AsyncSession
    ):
        result = await session.execute(select(func.count()).select_from(UserORM).filter(UserORM.id == id))
        count = result.scalar()

        if count > 0:
            return True

        return False

    @staticmethod
    async def get_user_id_by_login(
            login: str,
            session: AsyncSession
    ):
        user_id_record = await session.execute(
            select(User.id).select_from(User).filter(User.login == login)
        )

        return user_id_record.first().id

