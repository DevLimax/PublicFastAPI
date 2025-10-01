from fastapi import HTTPException, status
import re

class UniqueViolationException(HTTPException):
    def __init__(self, field: str, value):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe uma instancia com {field}: {field}, portanto não pode haver valores duplicados para esse campo"
        )

def NotNullViolationError(field: str, value):
    raise HTTPException(detail=f"O campo {field} deve ser preenchido", status_code=status.HTTP_400_BAD_REQUEST)