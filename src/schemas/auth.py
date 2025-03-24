import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, str_256, str_30
import datetime


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.Identity(), primary_key=True)
    email: Mapped[str_256]
    nickname: Mapped[str_30]
    registered_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
