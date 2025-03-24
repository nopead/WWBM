from src.schemas.hint import Hint as HintORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Tuple, Literal
from src.schemas.game import Game, GameAnswersHistory, Prize, GameFinishReason
from src.schemas.auth import User
from sqlalchemy import func
from src.models.result import LeaderBoardResult


class ResultsService:
    @staticmethod
    async def get(
            session: AsyncSession,
            offset: int = 0,
            limit: int = 100,
            sort_by: List[Tuple[
                Literal["games_amount", "wins_amount", "prize_amount"],
                Literal["asc", "desc"]
            ]] = [("prize_amount", "desc")]
    ):
        try:
            stmt = (select(
                    User.nickname,
                    func.count(Game.id).label("games_amount"),
                    func.count(Game.id).filter(Game.finish_reason == 3).label("wins_amount"),
                    func.sum(Prize.amount).label("prize_amount")
                ).select_from(Game)
                 .join(User, User.id == Game.player_id)
                    .join(Prize, Prize.id == Game.prize)
                    .group_by(User.nickname)
            )
            result = await session.execute(stmt)
            model_result = []
            placement = 1
            for record in result:
                model_result.append(
                    LeaderBoardResult(
                        placement=placement,
                        player=record.nickname,
                        games_amount=record.games_amount,
                        wins_amount=record.wins_amount,
                        prize_amount=record.prize_amount
                    )
                )

            return model_result
        except Exception as e:
            await session.rollback()
            raise e
