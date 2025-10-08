from pydantic import BaseModel, ConfigDict
from typing import Optional

class NoAuthenticatedError(BaseModel):
    detail: str = "Not authenticated"
    
class InternalServerError(BaseModel):
    detail: dict = {
        "error": "Internal Server Error",
        "msg": "Ocorreu um erro interno no servidor durante a operação",
    }
    
class ConflictError(BaseModel):
    detail: dict = {
        "Error": "Error",
        "msg": "string"
    }
    