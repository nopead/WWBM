from sqlalchemy.ext.asyncio import AsyncSession
from src.models.auth import UserLoginModel, UserRegistrationModel
from src.services.smtp import SMTPService, FakeSMTPService
from src.services.phone import PhoneService, FakePhoneService
from src.schemas.auth import VeificationCodes
from fastapi import HTTPException, Response, Request
from fastapi.responses import JSONResponse
from src.schemas.auth import User
from sqlalchemy import select
from authx import AuthX, TokenPayload
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
    async def get_sender_from_request(
            request: Request,
            security: AuthX
    ):
        token = await security.get_access_token_from_request(request)
        if not token:
            raise HTTPException(
                status_code=401,
                detail="unauthorized"
            )
        return security.verify_token(token=token).sub

    @staticmethod
    async def is_user_superuser(
        session: AsyncSession,
        login: str
    ):
        user_role_exec_result = await session.execute(
            select(User.is_superuser).select_from(User).filter(User.login == login)
        )

        return user_role_exec_result.first()

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
                    status_code=409,
                    content="invalid login or code"
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
    async def validate_login(
            creds: UserLoginModel,
            session: AsyncSession,
            security: AuthX
    ) -> Response:
        try:
            record = await session.get(VeificationCodes, creds.login)

            user_select_stmt = select(User.login).select_from(User).filter(User.login == creds.login)
            user = await session.execute(user_select_stmt)

            if not user.first():
                raise HTTPException(
                    status_code=404,
                    detail="user not found"
                )

            if not record:
                raise HTTPException(
                    status_code=404,
                    detail="invalid login or code"
                )
            else:
                if creds.verification_code == record.code:
                    await AuthService.delete_code_record(creds.login, session)
                    access_token = security.create_access_token(
                        uid=creds.login
                    )
                    return JSONResponse(
                        status_code=200,
                        headers={"access_token": access_token},
                        content="login successful"
                    )
                else:
                    return JSONResponse(
                        status_code=400,
                        content="invalid code"
                    )
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def validate_registration(
            creds: UserRegistrationModel,
            session: AsyncSession
    ) -> Response:
        try:

            record = await session.get(VeificationCodes, creds.login)
            user_select_statement = select(User.login).select_from(User).filter(User.login == creds.login)
            user = await session.execute(user_select_statement)

            if user.first():
                raise HTTPException(
                    status_code=409,
                    detail="login already used"
                )

            if not record:
                raise HTTPException(
                    status_code=409,
                    detail="invalid login or code"
                )
            else:
                if creds.verification_code == record.code:
                    new_user = User(
                        login=creds.login,
                        nickname=creds.login,
                        is_superuser=False
                    )

                    session.add(new_user)
                    await session.flush()
                    await session.commit()
                    await AuthService.delete_code_record(
                        login=creds.login,
                        session=session
                    )
                    return JSONResponse(
                        status_code=200,
                        content="successful registration"
                    )
                else:
                    return Response(
                        status_code=400,
                        content="invalid code"
                    )
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def delete_user(
            session: AsyncSession,
            payload: TokenPayload,
            login: str
    ):
        try:
            sender = payload.sub

            if not AuthService.is_user_superuser(
                    session=session,
                    login=sender):
                raise HTTPException(
                    status_code=403,
                    detail="forbidden"
                )
            else:
                user_to_delete = await session.execute(
                    select(User).filter(User.login == login)
                )
                user_to_delete = user_to_delete.scalars().first()
                await session.delete(user_to_delete)
                await session.commit()
                return Response(
                    status_code=200,
                    content="user deleted successfully"
                )
        except Exception as e:
            await session.rollback()
            raise e
