from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_session
from typing import List
from src.crud.results import ResultsService
from src.models.result import LeaderBoardResult


router = APIRouter(
    prefix="/results",
    tags=["Results"]
)


@router.get("/", response_model=List[LeaderBoardResult])
async def get(
        offset: int = 0,
        limit: int = 10,
        sort_by: List[str] = Query(
            ["prize_amount:desc"],
            description="Sorting criteria in format 'field:direction' (e.g., 'prize:asc')"
        ),
        session: AsyncSession = Depends(get_session)
):
    sort_params = []
    allowed_fields = {"games_amount", "wins_amount", "prize_amount"}
    allowed_directions = {"asc", "desc"}

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

        return await ResultsService.get(
            session=session,
            offset=offset,
            limit=limit,
            sort_by=sort_params
        )