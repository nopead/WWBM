from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.hint import HintSetter, HintGetter
from src.models.http_response import HTTPResponse
from src.crud.hints import HintService
from src.db.database import get_session


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


@router.get("/{hint_id}", response_model=HintGetter | HTTPResponse)
async def get_by_id(
        id: int,
        session: AsyncSession = Depends(get_session)
):
    return await HintService.get_by_id(
        id=id,
        session=session
    )


@router.post("/", response_model=HintSetter | HTTPResponse)
async def add(
        data: HintSetter,
        session: AsyncSession = Depends(get_session)
):
    return await HintService.add(
        data=data,
        session=session
    )


@router.put("/", response_model=HintGetter | HTTPResponse)
async def update(
        id: int,
        new_data: HintSetter,
        session: AsyncSession = Depends(get_session)
):
    return await HintService.update(
        id=id,
        new_data=new_data,
        session=session
    )


@router.delete("/{hint_id}", response_model=HTTPResponse)
async def delete(
        id: int,
        session: AsyncSession = Depends(get_session)
):
    return await HintService.delete(
        id=id,
        session=session
    )
