

class FakeSMTPService:
    @staticmethod
    async def send_code_mail(
            email: str,
            code: int
    ):
        pass


class SMTPService:
    ...
