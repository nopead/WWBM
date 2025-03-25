from authx import AuthXConfig, AuthX
from src.config import JWT_SECRET_KEY


auth_config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY=JWT_SECRET_KEY,
    JWT_TOKEN_LOCATION=["headers"],
    JWT_HEADER_TYPE="Bearer",
)

security = AuthX(config=auth_config)

