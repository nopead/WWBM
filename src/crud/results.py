import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Literal
from src.schemas.game import Game, GameAnswersHistory, Prize, GameFinishReason, HintsUseHistory
from src.schemas.auth import User
from src.schemas.question import Question, AnswersOnQuestion
from src.schemas.hint import Hint
from sqlalchemy import select, asc, desc, func, case, and_
from src.models.result import LeaderBoardResult, UserResult, UserResultDetail


class ResultsService:
    @staticmethod
    async def get(
            session: AsyncSession,
            offset: int = 0,
            limit: int = 10,
            sort_by: List[Tuple[
                Literal["games_amount", "wins_amount", "prize_amount"],
                Literal["desc", "asc"]
            ]] = [("prize_amount", "desc")]
    ):
        try:
            stmt = (select(
                            User.nickname,
                            func.count(Game.id).label("games_amount"),
                            func.count(Game.id).filter(Game.finish_reason == 3).label("wins_amount"),
                            func.sum(Prize.amount).label("prize_amount")
                        )
                    .select_from(Game)
                    .join(User, User.id == Game.player_id)
                    .join(Prize, Prize.id == Game.prize)
                    .group_by(User.nickname)
                    )

            stmt = stmt.offset(offset).limit(limit)

            for field, direction in sort_by:
                stmt = stmt.order_by(
                    asc(field) if direction == "asc" else desc(field)
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
                placement += 1

            return model_result
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_user_results(
            user_id: int,
            offset: int,
            limit: int,
            session: AsyncSession,
            sort_by: List[Tuple[
                Literal["prize", "duration", "questions_amount", "id", "date"],
                Literal["desc", "asc"]
            ]] = [("id", "desc")]
    ):
        try:
            stmt = (
                select(
                    Game.id,
                    func.date(Game.start_date).label("date"),
                    case(
                        (Game.end_date.is_not(None),
                         func.extract("epoch", Game.end_date - Game.start_date)),
                        else_=func.extract("epoch", func.now() - Game.start_date)
                    ).label("duration"),
                    func.count(GameAnswersHistory.game_id).label("questions_amount"),
                    GameFinishReason.name.label("result"),
                    Prize.amount.label("prize")
                )
                .select_from(Game)
                .join(GameAnswersHistory, GameAnswersHistory.game_id == Game.id)
                .join(GameFinishReason, GameFinishReason.id == Game.finish_reason)
                .join(Prize, Prize.id == Game.prize)
                .filter(Game.player_id == user_id)
                .group_by(
                    Game.id,
                    func.date(Game.start_date),
                    Game.end_date,
                    Game.start_date,
                    GameFinishReason.name,
                    Prize.amount
                )
                .offset(offset)
                .limit(limit)
            )

            for field, direction in sort_by:
                stmt = stmt.order_by(
                    asc(field) if direction == "asc" else desc(field)
                )

            result = await session.execute(stmt)

            result_models = []
            for record in result:
                result_models.append(
                    UserResult(
                        id=record.id,
                        date=record.date,
                        duration=int(record.duration),
                        questions_amount=record.questions_amount,
                        result=record.result,
                        prize=record.prize
                    )
                )

            return result_models
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_details(
            game_id: int,
            session: AsyncSession
    ):
        try:
            stmt = (
                select(
                    GameAnswersHistory.question_number.label("question_number"),
                    Question.text.label("question_text"),
                    select(AnswersOnQuestion.text).select_from(AnswersOnQuestion)
                        .filter(AnswersOnQuestion.question_id == Question.id)
                        .filter(AnswersOnQuestion.answer_id == GameAnswersHistory.answer)
                        .label("user_answer"),
                    select(AnswersOnQuestion.text).select_from(AnswersOnQuestion)
                        .filter(AnswersOnQuestion.question_id == Question.id)
                        .filter(AnswersOnQuestion.answer_id == Question.correct_answer)
                        .label("right_answer"),
                    Hint.name.label("hint"),
                    Prize.amount.label("prize")
                )
                .select_from(GameAnswersHistory).filter(GameAnswersHistory.game_id == game_id)
                .outerjoin(target=HintsUseHistory, onclause=and_(
                      HintsUseHistory.question_number == GameAnswersHistory.question_number,
                      HintsUseHistory.game_id == game_id))
                .outerjoin(target=Hint, onclause=Hint.id == HintsUseHistory.hint_id)
                .outerjoin(target=Prize, onclause=Prize.id == GameAnswersHistory.question_number + 1)
                .outerjoin(target=Question, onclause=GameAnswersHistory.question_id == Question.id)
            )

            records = await session.execute(stmt)

            result_models = []

            for record in records:
                result_models.append(
                    UserResultDetail(
                        question_number=record.question_number,
                        question_text=record.question_text,
                        user_answer=record.user_answer,
                        right_answer=record.right_answer,
                        hint="Нет" if not record.hint else record.hint,
                        prize=record.prize
                    )
                )

            return result_models
        except Exception as e:
            await session.rollback()
            raise e
