from datetime import datetime
from .base import MyBaseModel


class Prize(MyBaseModel):
    id: int
    amount: int


class GameFinishReason(MyBaseModel):
    id: int
    name: str


class Game(MyBaseModel):
    id: int
    player_id: int
    start_date: datetime
    end_date: datetime | None
    finish_reason: str | None
    prize: int


class HintsUseHistory(MyBaseModel):
    game_id: int
    hint_id: int
    question_number: int


class GameAnswersHistory(MyBaseModel):
    game_id: int
    question_number: int
    question_id: int
    answer_id: int

