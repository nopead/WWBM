from typing import List, Optional
from .base import MyBaseModel


class AnswerOnQuestion(MyBaseModel):
    answer_id: int
    text: str


class QuestionSetter(MyBaseModel):
    text: str
    hardness_level: int
    graphics_link: Optional[str]
    correct_answer: int
    answers: List[AnswerOnQuestion]


class QuestionGetter(QuestionSetter):
    id: int
