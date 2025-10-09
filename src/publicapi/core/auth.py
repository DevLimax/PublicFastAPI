import pytz
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from sqlalchemy.future import select
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from publicapi.models.userModel import UserModel
from publicapi.core.configs import settings
from publicapi.core.security import verify_password
from publicapi.utils.querys_db import search_all_items_in_db

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

async def authenticate(userInput: str,
                       password: str,
                       db: AsyncSession
) -> Optional[UserModel]:

    async with db as session:
        query = select(UserModel).where(
            or_(
                UserModel.username == userInput,
                UserModel.email == userInput
            )
        )
        result = await session.execute(query)
        user: Optional[UserModel] = result.scalars().unique().one_or_none()

        if not user:
            return None
        
        if not verify_password(password=password, hashed_password=user.password):
            return None
        
        await session.commit()
        await session.refresh(user)
        return user
    
def create_token(type_token: str, timelife: timedelta, sub: str) -> str:
    payload = {}
    sp = pytz.timezone("America/Sao_Paulo")
    expired = datetime.now(tz=sp) + timelife

    payload["type"] = type_token
    payload["exp"] = expired
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = sub
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_access_token(sub: str) -> str:
    return create_token(
        type_token="access_token",
        timelife=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRED),
        sub=sub
    )

def create_refresh_token(sub: str) -> str:
    return create_token(
        type_token="refresh_token",
        timelife=timedelta(days=12),
        sub=sub
    )

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        print(payload)
        return payload
    except jwt.JWTError as e:
        print(e)
        return None
    
def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.JWTError:
        return None