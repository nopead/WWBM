import datetime
from fastapi import HTTPException
from src.schemas.game import Game as GameORM, Prize as PrizeORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, desc
from typing import List, Literal, Tuple
from src.crud.users import UserService


class GameService:
    @staticmethod
    async def get(
            session: AsyncSession,
            offset: int = 0,
            limit: int = 100,
            sort_by: List[Tuple[
                Literal["start_date", "end_date", "amount"],
                Literal["asc", "desc"]
            ]] = [("start_date", "desc")]
    ):

        stmt = select(
            GameORM.id,
            GameORM.player_id,
            GameORM.start_date,
            GameORM.end_date,
            GameORM.finish_reason,
            PrizeORM.amount.label("prize_amount"),
        ).select_from(GameORM).join(PrizeORM, PrizeORM.id == GameORM.prize)

        column_map = {
            "start_date": GameORM.start_date,
            "end_date": GameORM.end_date,
            "amount": PrizeORM.amount
        }

        for field, direction in sort_by:
            column = column_map[field]
            stmt = stmt.order_by(
                desc(column) if direction == "desc" else asc(column)
            )

        stmt = stmt.offset(offset).limit(limit)

        games = await session.execute(stmt)

        return [
            GameORM(
                id=game.id,
                player_id=game.player_id,
                start_date=game.start_date,
                end_date=game.end_date,
                finish_reason=game.finish_reason,
                prize=game.prize_amount
            )
            for game in games]

    @staticmethod
    async def add(
            player_id: int,
            session: AsyncSession
    ):
        try:
            is_player_exists = await UserService.is_exists(
                id=player_id,
                session=session
            )

            print("checking player on exists")

            if not is_player_exists:
                raise HTTPException(
                    status_code=404,
                    detail="player not found"
                )

            print("player exists")

            existing_game = await session.execute(
                select(GameORM).where(
                    GameORM.player_id == player_id,
                    GameORM.end_date.is_(None),
                    GameORM.finish_reason.is_(None)
                )
            )

            if existing_game.scalar_one_or_none():
                raise HTTPException(
                    status_code=400,
                    detail="Player has an active unfinished game"
                )

            # Create new game if no active games exist
            new_game = GameORM(
                player_id=player_id,
                start_date=datetime.datetime.utcnow(),
                end_date=None,
                prize=1
            )
            session.add(new_game)
            await session.commit()
            await session.refresh(new_game)
            return new_game

        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def increase_prize(
            game_id: int,
            session: AsyncSession
    ):
        game_orm = await session.get(GameORM, game_id)
        if game_orm:
            if game_orm.prize < 16:
                game_orm.prize += 1
                await session.commit()
                return game_orm
        else:
            raise HTTPException(
                status_code=404,
                detail="game not found"
            )

    @staticmethod
    async def reset_prize(
            game_id: int,
            session: AsyncSession
    ):
        game_orm = await session.get(GameORM, game_id)
        if game_orm:
            game_orm.prize = 1
            await session.commit()
            return game_orm
        else:
            raise HTTPException(
                status_code=404,
                detail="game not found"
            )

    @staticmethod
    async def finish(game_id: int, finish_reason: int, session: AsyncSession):
        pass

    @staticmethod
    async def get_details(game_id: int, session: AsyncSession):
        pass
