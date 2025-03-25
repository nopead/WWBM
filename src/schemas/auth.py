import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
import datetime


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.Identity(), primary_key=True)
    login: Mapped[str]
    nickname: Mapped[str]
    registered_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    is_superuser: Mapped[bool] = mapped_column(nullable=False)


class VeificationCodes(Base):

    __tablename__ = "verification_codes"

    login: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    code: Mapped[int]

