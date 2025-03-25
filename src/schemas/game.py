import datetime
import sqlalchemy as sa
from sqlalchemy import ForeignKey, CheckConstraint, PrimaryKeyConstraint, text
from sqlalchemy.orm import Mapped, mapped_column
from src.schemas.auth import User
from .base import Base


class Prize(Base):
    __tablename__ = 'prizes'

    id: Mapped[int] = mapped_column(sa.Identity(), primary_key=True)
    amount: Mapped[int]


class GameFinishReason(Base):
    __tablename__ = 'game_finish_reason'

    id: Mapped[int] = mapped_column(sa.Identity(), primary_key=True)
    name: Mapped[str]


class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(sa.Identity(), primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    start_date: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    end_date: Mapped[datetime.datetime | None]
    finish_reason: Mapped[int] = mapped_column(ForeignKey("game_finish_reason.id"), nullable=True)
    prize: Mapped[int] = mapped_column(ForeignKey("prizes.id"), server_default="1")


class HintsUseHistory(Base):

    __tablename__ = 'hints_use_history'
    __table_args__ = (
        PrimaryKeyConstraint("game_id", "hint_id", "question_number", name="PK__hints_use_history"),
        CheckConstraint("question_number BETWEEN 1 AND 15", name="CK__hints_use_history__question_number"),
    )

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    hint_id: Mapped[int] = mapped_column(ForeignKey("hints.id"))
    question_number: Mapped[int]


class GameAnswersHistory(Base):

    __tablename__ = 'game_answers_history'
    __table_args__ = (
        PrimaryKeyConstraint("game_id", "question_number", "question_id", name="PK__game_answers_history"),
        CheckConstraint("question_number BETWEEN 1 AND 15", "CK__game_answers_history__question_number"),
        CheckConstraint("answer BETWEEN 1 AND 4", "CK__game_answers_history__answer"),
    )

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    question_number: Mapped[int]
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    answer: Mapped[int]
