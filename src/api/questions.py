from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_session
from src.models.question import QuestionGetter, QuestionSetter
from src.crud.questions import QuestionService

from typing import List


router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


@router.get("/all", response_model=List[QuestionGetter] | None)
async def get_all(
        offset: int = 0,
        limit: int = 10,
        session: AsyncSession = Depends(get_session)
):
    return await QuestionService.get(
        offset=offset,
        limit=limit,
        session=session
    )


@router.get("/random", response_model=QuestionGetter)
async def get_random(
    hardness_level: int = Query(..., ge=1, le=5),
    excluded_ids: list[int] = Query(
        default=[],
        description="Comma-separated list of question IDs to exclude",
        example="5,8,12"
    ),
    session: AsyncSession = Depends(get_session)
):
    return await QuestionService.get_random(
        hardness_level=hardness_level,
        excluded_ids=excluded_ids,
        session=session
    )


@router.post("/add", response_model=QuestionSetter | None)
async def add(
        data: QuestionSetter,
        session: AsyncSession = Depends(get_session)
):
    return await QuestionService.add(
        data=data,
        session=session
    )
