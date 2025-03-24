from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_session
from typing import List
from src.crud.results import ResultsService
from src.models.result import LeaderBoardResult, UserResult, UserResultDetail


router = APIRouter(
    prefix="/results",
    tags=["Results"]
)


async def get_sort_params(sort_by, allowed_fields, allowed_directions):
    sort_params = []
    for param in sort_by:
        if ":" not in param:
            field, direction = param, "desc"
        else:
            field, direction = param.split(":", 1)

        field = field.lower()
        direction = direction.lower()

        if field not in allowed_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid sort field '{field}'. Allowed fields: {', '.join(allowed_fields)}"
            )

        if direction not in allowed_directions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid sort direction '{direction}'. Use 'asc' or 'desc'"
            )

        sort_params.append((field, direction))
    return sort_params

@router.get("/leaderboard", response_model=List[LeaderBoardResult])
async def get(
        offset: int = 0,
        limit: int = 10,
        sort_by: List[str] = Query(
            ["prize_amount:desc"],
            description="Sorting criteria in format 'field:direction' (e.g., 'prize:asc')"
        ),
        session: AsyncSession = Depends(get_session)
):
    try:

        allowed_fields = {"games_amount", "wins_amount", "prize_amount"}
        allowed_directions = {"asc", "desc"}

        sort_params = await get_sort_params(
            sort_by=sort_by,
            allowed_fields=allowed_fields,
            allowed_directions=allowed_directions
        )

        return await ResultsService.get(
            session=session,
            offset=offset,
            limit=limit,
            sort_by=sort_params
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my", response_model=List[UserResult])
async def get_my_results(
        user_id: int,
        offset: int = 0,
        limit: int = 10,
        session: AsyncSession = Depends(get_session),
        sort_by: List[str] = Query(
            ["prize:desc"],
            description="Sorting criteria in format 'field:direction' (e.g., 'prize:asc')"
        )
):
    allowed_fields = {"id", "date", "prize", "duration", "questions_amount", "result"}
    allowed_directions = {"asc", "desc"}

    sort_params = await get_sort_params(
        sort_by=sort_by,
        allowed_fields=allowed_fields,
        allowed_directions=allowed_directions
    )

    return await ResultsService.get_user_results(
        user_id=user_id,
        offset=offset,
        limit=limit,
        session=session,
        sort_by=sort_params
    )


@router.get("/my/details/{game_id}", response_model=List[UserResultDetail])
async def get_game_details(
        game_id: int,
        session: AsyncSession = Depends(get_session)
):
    pass