import datetime
from sqlalchemy import ForeignKey, CheckConstraint, PrimaryKeyConstraint, text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, str_50


class GameFinishReason(Base):
    __tablename__ = 'game_finish_reason'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_50]


class Game(Base):
    __tablename__ = 'game'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column("user.id")
    start_date: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    end_date: Mapped[datetime.datetime]
    finish_reason: Mapped[int] = mapped_column(ForeignKey("game_finish_reason.id"))
    prize: Mapped[int] = mapped_column(server_default=text("0"))


class HintsUseHistory(Base):

    __tablename__ = 'hints_use_history'
    __table_args__ = (
        PrimaryKeyConstraint("game_id", "hint_id", name="PK__hints_use_history"),
        CheckConstraint("question_number BETWEEN 1 AND 15", name="CK__hints_use_history__question_number"),
    )

    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    hint_id: Mapped[int] = mapped_column(ForeignKey("hint.id"))
    question_number: Mapped[int]


class GameAnswersHistory(Base):

    __tablename__ = 'game_answers_history'
    __table_args__ = (
        PrimaryKeyConstraint("game_id", "question_number", name="PK__game_answers_history"),
        CheckConstraint("question_number BETWEEN 1 AND 15", "CK__game_answers_history__question_number"),
        CheckConstraint("answer BETWEEN 1 AND 4", "CK__game_answers_history__answer"),
    )

    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    question_number: Mapped[int]
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    answer: Mapped[int]
