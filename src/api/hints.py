import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.hint import Hint, HintData
from src.crud.hints import get_hints, get_hint_by_id, add_new_hint, update_hint, delete_hint
from src.db.database import get_session


router = APIRouter(
    prefix="/hints",
    tags=["hints"]
)


@router.get("/", response_model=list[Hint] | dict)
async def get_all(offset: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    try:
        hints = await get_hints(offset=offset, limit=limit, session=session)
    except sqlalchemy.exc.InternalError:
        raise HTTPException(status_code=404, detail="hint not found")
    return hints


@router.get("/{hint_id}", response_model=HintData | dict)
async def get_by_id(hint_id: int, session: AsyncSession = Depends(get_session)):
    try:
        hint = await get_hint_by_id(hint_id=hint_id, session=session)
        if not hint:
            raise HTTPException(status_code=404, detail="no hints found")
    except sqlalchemy.exc.InternalError:
        raise HTTPException(status_code=500, detail="internal server error")
    return hint


@router.post("/", response_model=Hint | dict)
async def add_new(hint: HintData, session: AsyncSession = Depends(get_session)):
    try:
        result = await add_new_hint(hint, session)
        return result
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=500, detail="internal server error")


@router.put("/", response_model=Hint | dict)
async def update(hint_id: int, new_data: HintData, session: AsyncSession = Depends(get_session)):
    try:
        updated_hint = await update_hint(hint_id=hint_id, new_data=new_data, session=session)
        if not updated_hint:
            raise HTTPException(status_code=501, detail="bad request")
        return updated_hint
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=500, detail="internal server error")


@router.delete("/{hint_id}", response_model=dict)
async def delete(hint_id: int, session: AsyncSession = Depends(get_session)):
    try:
        await delete_hint(hint_id, session)
        return {"status_code": 200, "details": "hint deleted successfully"}
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=500, detail="internal server error")

