from pydantic import BaseModel, ConfigDict
from typing import Optional

class NoAuthenticatedResponse(BaseModel):
    detail: str = "Not authenticated"
    
class InternalServerResponse(BaseModel):
    detail: dict = {
        "error": "Internal Server Error",
        "msg": "String",
    }
    
class ConflictResponse(BaseModel):
    detail: dict = {
        "Error": "Error",
        "msg": "string"
    }

class NotFoundResponse(BaseModel):
    detail: str = "String"
    