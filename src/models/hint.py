from .base import MyBaseModel
from typing import Optional


class Hint(MyBaseModel):
    id: int
    name: str
    icon_link: Optional[str]


class HintData(MyBaseModel):
    name: str
    icon_link: Optional[str]