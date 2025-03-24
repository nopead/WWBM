from src.models.base import MyBaseModel
from datetime import date, time


class LeaderBoardResult(MyBaseModel):
    placement: int
    player: str
    games_amount: int
    wins_amount: int
    prize_amount: int


class UserResult(MyBaseModel):
    game_id: int
    game_date: date
    start_time: time
    end_time: time
    questions_amount: int
    result: str
    prize: int


class UserResultDetail(MyBaseModel):
    question_id: int
    question_text: str
    user_answer: str
    rigth_answer: str
    hint: str
    prize: int