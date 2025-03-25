import datetime

from src.models.base import MyBaseModel
from datetime import datetime


class User(MyBaseModel):
    id: int
    login: str
    nickname: str
    registered_at: datetime
    is_superuser: bool


class UserLoginModel(MyBaseModel):
    login: str
    verification_code: int


class UserRegistrationModel(MyBaseModel):
    login: str
    nickname: str
    verification_code: int
