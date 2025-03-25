from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_session
from src.crud.auth import AuthService
from src.models.auth import UserLoginModel, UserRegistrationModel
from authx import TokenPayload
from src.api.security import security

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/send_verification_code/{login}")
async def send_verification_code(
        login: str,
        session: AsyncSession = Depends(get_session)
):
    return await AuthService.set_verification_code(
        login=login,
        session=session
    )


@router.post("/login")
async def login(
        creds: UserLoginModel,
        session: AsyncSession = Depends(get_session)
):
    return await AuthService.validate_login(
        creds=creds,
        session=session,
        security=security
    )


@router.post("/registrate")
async def registrate(
        creds: UserRegistrationModel,
        session: AsyncSession = Depends(get_session)
):
    return await AuthService.validate_registration(
        creds=creds,
        session=session
    )


@router.delete("/delete_user/{login}")
async def delete_user(
        login: str,
        session: AsyncSession = Depends(get_session),
        payload: TokenPayload = Depends(security.access_token_required)
):
    return await AuthService.delete_user(
        session=session,
        payload=payload,
        login=login
    )

