class InviteLimitExceeded(PermissionError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UserDoesNotExist(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)