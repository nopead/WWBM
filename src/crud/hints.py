from src.schemas.hint import Hint as HintORM
from src.models.hint import HintData as HintDataModel, Hint as HintModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError


async def get_hints(offset: int, limit: int, session: AsyncSession):
    stmt = select(HintORM).offset(offset).limit(limit)
    result = await session.execute(stmt)
    hints = result.scalars().all()
    return hints


async def get_hint_by_id(hint_id: int, session: AsyncSession):
    stmt = select(HintORM).filter(HintORM.id == hint_id)
    result = await session.execute(stmt)
    hint = result.scalars().first()
    return hint


async def add_new_hint(new_hint: HintDataModel, session: AsyncSession):
    result = None
    try:
        new_hint_inst = HintORM(name=new_hint.name, icon_link=new_hint.icon_link)
        session.add(new_hint_inst)
        await session.flush()
        await session.commit()
        result = new_hint_inst
    except SQLAlchemyError as e:
        result = {"status_code": 503, "detail": "hint create failed"}
        error = str(e.__cause__)
        await session.rollback()
        raise RuntimeError(error) from e
    finally:
        await session.close()
        print(type(result))
        return result


async def update_hint(hint_id: int, new_data: HintDataModel, session: AsyncSession):
    hint = await session.get(HintORM, hint_id)
    if hint:
        try:
            hint.name = new_data.name
            hint.icon_link = new_data.icon_link
            await session.commit()
            return hint
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            raise RuntimeError(error) from e
        finally:
            await session.close()


async def delete_hint(hint_id: int, session: AsyncSession):
    select_stmt = select(HintORM).filter(HintORM.id == hint_id)
    select_result = await session.execute(select_stmt)
    hint = select_result.scalars().first()
    if hint:
        try:
            await session.delete(hint)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
        finally:
            await session.close()
            return None
