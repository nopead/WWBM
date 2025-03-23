from .base import MyBaseModel


class HTTPResponse(MyBaseModel):
    status_code: int
    detail: str
