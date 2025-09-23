from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from publicapi.core.auth import authenticate, create_access_token, create_refresh_token, verify_refresh_token
from publicapi.core.deps import get_session, get_current_user
from publicapi.core.security import generate_hashed_password
from publicapi.schemas.userSchema import AuthResponse, UserSchemaBase, UserSchemaCreate
from publicapi.utils.querys_db import search_item_in_db
from publicapi.models import UserModel

router = APIRouter()

@router.get("/logged", response_model=UserSchemaBase, status_code=status.HTTP_200_OK)
async def logged_user(user: UserSchemaBase = Depends(get_current_user)):
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")    
    return user

@router.post("/sign-in", response_model=UserSchemaBase, status_code=status.HTTP_201_CREATED)
async def create(data: UserSchemaCreate,
                 db: AsyncSession = Depends(get_session)
) -> UserSchemaBase:
    async with db as session:       

        new_user = UserModel(
            username = data.username,
            email = data.email,
            password = generate_hashed_password(data.password)
        )
    
        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        
        except IntegrityError as e:
            error_str = str(e.orig)
            if "email" in error_str:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
            elif "username" in error_str:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_session)
) -> AuthResponse:
    
    user = await authenticate(userInput=form_data.username, 
                              password=form_data.password, 
                              db=db
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    data = AuthResponse(
        access_token = create_access_token(sub=str(user.id)),
        refresh_token = create_refresh_token(sub=str(user.id))
    )
    return data

@router.post("/refresh-token", response_model=AuthResponse)
async def refresh_token(refresh_token: str = Form(...),
                        db: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """
    Endpoint para criar um novo access_token apartir do (refresh_token)
    """
    payload = verify_refresh_token(token=refresh_token)
    if not payload or payload.get("type") != "refresh_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token Inválido"
        )
    
    username = payload.get("sub")
    new_access_token: str = create_access_token(sub=username)
    new_refresh_token: str = create_refresh_token(sub=username)
    data = AuthResponse(
        access_token = new_access_token,
        refresh_token = new_refresh_token
    )
 
    return data
    
