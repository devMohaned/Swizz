from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, code: str, message: str, status_code: int):
        super().__init__(
            status_code=status_code,
            detail={
                "code": code,
                "message": message,
                "status": status_code
            }
        )


class DuplicateUserException(AppException):
    def __init__(self):
        super().__init__(
            code="DUPLICATE_USER",
            message="User with this email already exists.",
            status_code=status.HTTP_409_CONFLICT
        )
