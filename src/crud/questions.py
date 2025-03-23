from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from src.models.question import QuestionSetter as QuestionSetterModel, QuestionGetter as QuestionGetterModel, AnswerOnQuestion as AnswerOnQuestionModel
from src.schemas.question import Question as QuestionORM, AnswersOnQuestion as AnswersOnQuestionORM


class QuestionService:
    @staticmethod
    async def get(offset: int, limit: int, session: AsyncSession):
        try:
            stmt = select(QuestionORM).offset(offset).limit(limit)
            result = await session.execute(stmt)
            questions_orm = result.scalars().unique().all()

            questions = []
            for q_orm in questions_orm:
                answers = [
                    AnswerOnQuestionModel(
                        answer_id=answer.answer_id,
                        text=answer.text
                    )
                    for answer in q_orm.answers
                ]

                questions.append(QuestionGetterModel(
                    id=q_orm.id,
                    text=q_orm.text,
                    hardness_level=q_orm.hardness_level,
                    graphics_link=q_orm.graphics_link,
                    correct_answer=q_orm.correct_answer,
                    answers=answers
                ))

            return questions
        except Exception as e:
            await session.rollback()
            raise e


    @staticmethod
    async def add(data: QuestionSetterModel, session: AsyncSession):
        try:
            question_data = data.model_dump(exclude={'answers'})
            question_orm = QuestionORM(**question_data)

            for answer in data.answers:
                answer_data = answer.model_dump()
                answer_orm = AnswersOnQuestionORM(**answer_data)
                question_orm.answers.append(answer_orm)

            session.add(question_orm)
            await session.flush()
            await session.commit()
            return data
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_random(
        hardness_level: int,
        excluded_ids: list[int],
        session: AsyncSession
    ):
        try:
            stmt = (
                select(QuestionORM)
                .where(
                    QuestionORM.hardness_level == hardness_level,
                    QuestionORM.id.notin_(excluded_ids) if excluded_ids else True
                )
                .order_by(func.random())
                .limit(1)
            )

            result = await session.execute(stmt)
            question_orm = result.unique().scalar_one_or_none()

            if not question_orm:
                return None

            return QuestionGetterModel(
                id=question_orm.id,
                text=question_orm.text,
                hardness_level=question_orm.hardness_level,
                graphics_link=question_orm.graphics_link,
                correct_answer=question_orm.correct_answer,
                answers=[
                    AnswerOnQuestionModel(
                        answer_id=answer.answer_id,
                        text=answer.text
                    )
                    for answer in question_orm.answers
                ]
            )
        except SQLAlchemyError as e:
            await session.rollback()
            raise e