from sqlalchemy.ext.asyncio import AsyncSession
from src.models.auth import UserLoginModel, UserRegistrationModel
from src.services.smtp import SMTPService, FakeSMTPService
from src.services.phone import PhoneService, FakePhoneService
from src.schemas.auth import VeificationCodes
from fastapi import HTTPException, Response
import random
import re


class CredentialsValidator:
    @staticmethod
    async def validate_email(
            email: str
    ) -> bool:
        email_regex = re.compile(r'''(
                    [a-zA-Z0-9._%+-]+
                    @ 
                    [a-zA-Z0-9.-]+
                    (\.[a-zA-Z]{2,4})
                    )''', re.VERBOSE)

        return bool(email_regex.match(email))

    @staticmethod
    async def validate_phone(
            phone_number: str
    ) -> bool:
        phone_regex = re.compile(r'''^(8|\+7)[\d]{10}''')

        return bool(phone_regex.match(phone_number))


class AuthService:
    @staticmethod
    async def add_code_record(
            login: str,
            code: int,
            session: AsyncSession
    ):
        try:

            new_code_record = VeificationCodes(
                login=login,
                code=code
            )

            record = await session.get(VeificationCodes, login)

            if not record:
                session.add(new_code_record)
                await session.flush()
                await session.commit()
            else:
                record.code = code
                await session.commit()

        except Exception as e:
            await session.close()
            raise e

    @staticmethod
    async def delete_code_record(
            login: str,
            session: AsyncSession
    ):
        try:
            record = await session.get(VeificationCodes, login)
            if record:
                await session.delete(record)
                await session.commit()
                return Response(
                    status_code=200,
                    content="deleted successfully"
                )
            else:
                return Response(
                    status_code=404,
                    content="user has no verification codes"
                )
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def set_verification_code(
            login: str,
            session: AsyncSession
    ):
        code = random.randint(1000, 9999)
        try:
            if await CredentialsValidator.validate_email(login):
                await FakeSMTPService.send_code_mail(
                    email=login,
                    code=code
                )
            elif await CredentialsValidator.validate_phone(login):
                await FakePhoneService.send_code_sms(
                    phone_number=login,
                    code=code
                )
            else:
                raise HTTPException(
                    status_code=501,
                    detail="invalid data"
                )

            await AuthService.add_code_record(
                login=login,
                code=code,
                session=session
            )

            return Response(
                status_code=200,
                content="code sended successfully"
            )

        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def login_code(
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

