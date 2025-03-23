from sqlalchemy import ForeignKey, CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import List


class Question(Base):

    __tablename__ = "question"
    __table_args__ = (
        CheckConstraint("hardness_level BETWEEN 1 AND 3", "CK__question__hardness_level"),
        CheckConstraint("correct_answer BETWEEN 1 AND 4", "CK__question__correct_answer"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    hardness_level: Mapped[int]
    graphics_link: Mapped[str | None]
    correct_answer: Mapped[int]

    answers: Mapped[List["AnswersOnQuestion"]] = relationship(
        back_populates="question",
        lazy="selectin",
        cascade="all, delete-orphan"
    )


class AnswersOnQuestion(Base):

    __tablename__ = "answers_on_question"
    __table_args__ = (
        PrimaryKeyConstraint("question_id", "answer_id", name="PK__answers_on_question"),
        CheckConstraint("answer_id BETWEEN 1 AND 4", "CK__answers_on_question__answer_id"),
    )

    answer_id: Mapped[int]
    text: Mapped[str]
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))

    question: Mapped["Question"] = relationship(
        back_populates="answers",
        lazy="selectin"
    )

