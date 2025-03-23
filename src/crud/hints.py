from src.schemas.hint import Hint as HintORM
from src.models.hint import HintSetter as HintDataModel
from src.models.http_response import HTTPResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class HintService:
    @staticmethod
    async def get_hints(offset: int, limit: int, session: AsyncSession):
        try:
            stmt = select(HintORM).offset(offset).limit(limit)
            result = await session.execute(stmt)
            hints = result.scalars().all()
            return hints
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_by_id(hint_id: int, session: AsyncSession):
        try:
            stmt = select(HintORM).filter(HintORM.id == hint_id)
            hint = await session.execute(stmt)
            return hint.scalars().first()
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def add(new_hint: HintDataModel, session: AsyncSession):
        try:
            new_hint_inst = HintORM(name=new_hint.name, icon_link=new_hint.icon_link)
            session.add(new_hint_inst)
            await session.flush()
            await session.commit()
            return new_hint_inst
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def update(hint_id: int, new_data: HintDataModel, session: AsyncSession):
        hint = await session.get(HintORM, hint_id)
        if hint:
            try:
                hint.name = new_data.name
                hint.icon_link = new_data.icon_link
                await session.commit()
                return hint
            except Exception as e:
                await session.rollback()
                raise e
        else:
            return HTTPResponse(status_code=404, detail="hint not found")

    @staticmethod
    async def delete(hint_id: int, session: AsyncSession):
        select_stmt = select(HintORM).filter(HintORM.id == hint_id)
        select_result = await session.execute(select_stmt)
        hint = select_result.scalars().first()
        if hint:
            try:
                await session.delete(hint)
                await session.commit()
                return HTTPResponse(status_code=200, detail="hint deleted successfully")
            except Exception as e:
                await session.rollback()
                raise e
        else:
            return HTTPResponse(status_code=404, detail="hint not found")
