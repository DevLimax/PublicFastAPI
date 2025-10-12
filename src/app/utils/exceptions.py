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

class NotFoundException(HTTPException):
    def __init__(self, id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instancia com id ({id}) não encontrada!"
        )

class InternalServerException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno do servidor durante operação"
        )
        
class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Usuário com pemissões insuficientes para realizar essa operação"
        )