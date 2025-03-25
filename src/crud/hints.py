from src.schemas.hint import Hint as HintORM
from src.models.hint import HintSetter as HintDataModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Response
from src.crud.auth import AuthService
from authx import TokenPayload


class HintService:
    @staticmethod
    async def get_hints(
            offset: int,
            limit: int,
            session: AsyncSession
    ):
        try:
            stmt = select(HintORM).offset(offset).limit(limit)
            result = await session.execute(stmt)
            hints = result.scalars().all()
            return hints
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_by_id(
            id: int,
            session: AsyncSession
    ):
        try:
            stmt = select(HintORM).filter(HintORM.id == id)
            hint = await session.execute(stmt)
            return hint.scalars().first()
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def add(
            data: HintDataModel,
            session: AsyncSession,
            payload: TokenPayload
    ):
        try:
            if not AuthService.is_user_superuser(
                    session=session,
                    login=payload.sub
            ):
                raise HTTPException(
                    status_code=403,
                    detail="Forbidden"
                )
            else:
                new_hint_inst = HintORM(name=data.name, icon_link=data.icon_link)
                session.add(new_hint_inst)
                await session.flush()
                await session.commit()
                return new_hint_inst
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def update(
            id: int,
            new_data: HintDataModel,
            session: AsyncSession,
            payload: TokenPayload
    ):
        try:
            hint = await session.get(HintORM, id)
            if hint:
                if not AuthService.is_user_superuser(
                        session=session,
                        login=payload.sub
                ):
                    raise HTTPException(
                        status_code=403,
                        detail="Forbidden"
                    )
                else:
                    hint.name = new_data.name
                    hint.icon_link = new_data.icon_link
                    await session.commit()
                    return Response(
                        status_code=200,
                        content="hint updated successfully"
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="hint not found"
                )
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def delete(
            id: int,
            session: AsyncSession,
            payload: TokenPayload
    ):
        try:
            if not AuthService.is_user_superuser(
                    session=session,
                    login=payload.sub
            ):
                raise HTTPException(
                    status_code=403,
                    detail="Forbidden"
                )
            else:
                select_stmt = select(HintORM).filter(HintORM.id == id)
                select_result = await session.execute(select_stmt)
                hint = select_result.scalars().first()
                if hint:
                    await session.delete(hint)
                    await session.commit()
                    return Response(
                        status_code=200,
                        content="hint deleted successfully"
                    )
                else:
                    raise HTTPException(
                        status_code=404,
                        detail="hint not found"
                    )
        except Exception as e:
            await session.rollback()
            raise e
