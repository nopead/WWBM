import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.hint import Hint, HintData
from src.crud.hints import get_hints, get_hint_by_id, add_new_hint, update_hint
from src.db.database import get_session


router = APIRouter(
    prefix="/hints",
    tags=["hints"]
)


@router.get("/", response_model=list[Hint])
def get_all(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    try:
        hints = get_hints(offset=offset, limit=limit, session=session)
    except sqlalchemy.exc.InternalError:
        return """{"status_code": 404, "details": "hints not found"}"""
    return hints


@router.get("/{hint_id}", response_model=str | HintData)
def get_by_id(hint_id: int, session: Session = Depends(get_session)):
    try:
        hint = get_hint_by_id(hint_id=hint_id, session=session)
        if not hint:
            raise HTTPException(status_code=404, detail="no hints found")
    except sqlalchemy.exc.InternalError:
        return """{"status_code": 404, "details": "hint not found"}"""
    return hint


@router.post("/", response_model=str | HintData)
def add_new(hint: HintData, session: Session = Depends(get_session)):
    try:
        hint = add_new_hint(hint, session=session)
    except sqlalchemy.exc.IntegrityError:
        return """{"status_code": 500, "details": "hint add error"}"""
    return hint


@router.put("/", response_model=str | Hint)
def update(hint_id: int, new_data: HintData, session: Session = Depends(get_session)):
    try:
        hint = update_hint(hint_id=hint_id, new_data=new_data, session=session)
    except sqlalchemy.exc.IntegrityError:
        return """{"status_code": 500, "details": "hint add error"}"""
    return hint
