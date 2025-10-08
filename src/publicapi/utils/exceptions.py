from fastapi import HTTPException, status
import re

class UniqueViolationException(HTTPException):
    def __init__(self, field: str, value):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "Unique Violation Error",
                "msg": f"ja existe uma instancia com o valor ({field}={value})!"
            }
        )

class ConflictException(HTTPException):
    def __init__(self, fields: list, values: list):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "Unique Constraint Error",
                "msg": f"ja existe uma instancia com os valores: ({dict(zip(fields, values))})!"
            }
        )