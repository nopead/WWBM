from fastapi import APIRouter, Depends, Response
from authx import AuthXConfig, AuthX
from src.config import JWT_SECRET_KEY
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_session
from src.crud.auth import AuthService
from src.models.auth import UserLoginModel, UserRegistrationModel


auth_config = AuthXConfig()
auth_config.JWT_SECRET_KEY = JWT_SECRET_KEY
auth_config.JWT_ACCESS_COOKIE_NAME = "wwbm_user"
auth_config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=auth_config)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/send_verification_code")
async def send_verification_code(
        login: str,
        session: AsyncSession = Depends(get_session)):
    return await AuthService.set_verification_code(
        login=login,
        session=session
    )


@router.post("/login")
async def login(
        data: UserLoginModel,
        response: Response
):
    pass