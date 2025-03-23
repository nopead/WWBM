from .base import MyBaseModel
from typing import Optional


class HintSetter(MyBaseModel):
    name: str
    icon_link: Optional[str]


class HintGetter(HintSetter):
    id: int