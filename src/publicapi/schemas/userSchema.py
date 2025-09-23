from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    created_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    
    class Config:
        from_attributes = True
        
class UserSchemaCreate(UserSchemaBase):
    password: str 

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str