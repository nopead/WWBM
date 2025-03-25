from sqlalchemy.ext.asyncio import AsyncSession
import random

class AuthService:
    @staticmethod
    async def set_verification_code(
            login: str,
            session: AsyncSession
    ):
        code = random.randint(1000, 9999)
        try:
            ...
            """ if login is email:
               await SMTPService.send_code_mail(
                   email=login,
                   code=code
               )
            else:
                await PhoneService.send_code_sms(
                    phone_number=login,
                    code=code
                )
            """
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def validate_verification_code(
            creds: UserLoginModel,
            session: AsyncSession
    ):
        pass

    @staticmethod
    async def register_user(
            creds: UserRegistrationModel,
            session: AsyncSession
    ):
        pass

    @staticmethod
    async def delete_user():
        pass

