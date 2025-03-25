from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.hint import HintSetter, HintGetter
from src.crud.hints import HintService
from src.db.database import get_session
from src.api.security import security
from authx import TokenPayload


router = APIRouter(
    prefix="/hints",
    tags=["hints"]
)


@router.get("/", response_model=list[HintGetter])
async def get(
        offset: int = 0,
        limit: int = 10,
        session: AsyncSession = Depends(get_session)
):
    return await HintService.get_hints(
        offset=offset,
        limit=limit,
        session=session
    )


@router.get("/{hint_id}", response_model=HintGetter | None)
async def get_by_id(
        id: int,
        session: AsyncSession = Depends(get_session)
):
    return await HintService.get_by_id(
        id=id,
        session=session
    )


@router.post("/", response_model=HintSetter | None)
async def add(
        data: HintSetter,
        session: AsyncSession = Depends(get_session),
        payload: TokenPayload = Depends(security.access_token_required),
):
    return await HintService.add(
        data=data,
        session=session,
        payload=payload
    )


@router.put("/", response_model=HintGetter | None)
async def update(
        id: int,
        new_data: HintSetter,
        session: AsyncSession = Depends(get_session),
        payload: TokenPayload = Depends(security.access_token_required),
):
    return await HintService.update(
        id=id,
        new_data=new_data,
        session=session,
        payload=payload
    )


@router.delete("/{hint_id}", response_model=None)
async def delete(
        id: int,
        session: AsyncSession = Depends(get_session),
        payload: TokenPayload = Depends(security.access_token_required),
):
    return await HintService.delete(
        id=id,
        session=session,
        payload=payload
    )
