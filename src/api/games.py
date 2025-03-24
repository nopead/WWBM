from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from src.models.game import Game, GameAnswersHistory
from src.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.games import GameService


router = APIRouter(
    prefix="/games",
    tags=["games"]
)


@router.get("/", response_model=List[Game])
async def get(
        offset: int = 0,
        limit: int = 10,
        sort_by: List[str] = Query(
            ["start_date:desc"],
            description="Sorting criteria in format 'field:direction' (e.g., 'prize:asc')"
        ),
        session: AsyncSession = Depends(get_session)
):
    try:
        sort_params = []
        allowed_fields = {"start_date", "end_date", "prize_amount"}
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

        return await GameService.get(
            session=session,
            offset=offset,
            limit=limit,
            sort_by=sort_params
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=Game)
async def register_new_game(
        player_id: int,
        session: AsyncSession = Depends(get_session)
):
    return await GameService.add(
        player_id=player_id,
        session=session
    )


@router.post("/update-prize")
async def increase_prize(
        game_id: int,
        session: AsyncSession = Depends(get_session)
):
    return await GameService.increase_prize(
        game_id,
        session
    )


@router.post("/reset-prize")
async def reset_prize(
        game_id: int,
        session: AsyncSession = Depends(get_session)
):
    return await GameService.reset_prize(
        game_id=game_id,
        session=session
    )


@router.post("/add-answer-in-history")
async def add_answer_in_history(
        data: GameAnswersHistory,
        session: AsyncSession = Depends(get_session)
):
    return await GameService.add_answer_in_history(
        data=data,
        session=session
    )


@router.post("/finish/{game_id}", response_model=Game)
async def finish(
        id: int,
        finish_reason: int,
        session: AsyncSession = Depends(get_session)
):
    return await GameService.finish(
        id=id,
        finish_reason=finish_reason,
        session=session
    )
