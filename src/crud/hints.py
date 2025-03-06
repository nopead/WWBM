import fastapi.exceptions
import sqlalchemy.exc

from src.schemas.hint import Hint as HintORM
from src.models.hint import HintData as HintDataModel, Hint as HintModel
from sqlalchemy.orm import Session


def get_hints(offset: int, limit: int, session: Session):
    hints = session.query(HintORM).offset(offset).limit(limit).all()
    return hints


def get_hint_by_id(hint_id: int, session: Session):
    hint = session.query(HintORM).filter(HintORM.id == hint_id).first()
    return hint


def add_new_hint(new_hint: HintDataModel, session: Session):
    hint_orm_obj = HintORM(**new_hint.dict())
    session.add(hint_orm_obj)
    session.commit()
    session.refresh(hint_orm_obj)
    return HintModel.model_validate(obj=hint_orm_obj, from_attributes=True)


def update_hint(hint_id: int, new_data: HintDataModel, session: Session):
    data = session.query(HintORM).filter(HintORM.id == hint_id).first()

    for field, value in new_data.dict().items():
        if not value == getattr(data, field):
            setattr(data, field, value)

    session.commit()
    session.refresh(data)
    return data