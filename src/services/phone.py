class PhoneService:
    pass


class FakePhoneService:
    @staticmethod
    async def send_code_sms(
            phone_number: str,
            code: int
    ):
        pass
