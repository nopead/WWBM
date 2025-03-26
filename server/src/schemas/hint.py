import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Hint(Base):

    __tablename__ = 'hints'

    id: Mapped[int] = mapped_column(sa.Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    icon_link: Mapped[str] = mapped_column(nullable=True)
