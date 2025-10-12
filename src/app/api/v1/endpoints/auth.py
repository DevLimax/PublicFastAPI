from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.auth import authenticate, create_access_token, create_refresh_token, verify_refresh_token
from app.core.deps import get_session, get_current_user
from app.core.security import generate_hashed_password
from app.schemas.userSchema import AuthResponse, UserSchemaBase, UserSchemaCreate, UserLoginSchema, UserRefreshTokenSchema
from app.schemas.ResponseSchema import NoAuthenticatedResponse
from app.utils.querys_db import search_item_in_db
from app.models import UserModel

router = APIRouter()

@router.get("/logged", 
            response_model=UserSchemaBase, 
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "model": NoAuthenticatedResponse,
                    "description": "Error de autenticação"
                }
            })
async def logged_user(user: UserSchemaBase = Depends(get_current_user)):
    """
    Endpoint com metodo GET, responsavel por verificar o usuário logado e retornar os dados.
    """
    return user

@router.post("/sign-in", 
             summary="Criar Usuário",
             response_model=UserSchemaBase, 
             status_code=status.HTTP_201_CREATED)
async def create(data: UserSchemaCreate,
                 db: AsyncSession = Depends(get_session)
) -> UserSchemaBase:
    """
    Endpoint com metodo POST, responsavel por criar uma instancia na tabela (usuarios)

    Para a criação de uma instancia (usuario), não é necessario que o usuário esteja logado no sistema.

    O endpoint requer:
    - username (nome de usuário)
    - email (email do usuário)
    - password (senha do usuário)

    caso esteja faltando algum dos campos obrigatorios, o endpoint irá retornar 422 (Unprocessable Entity).
    

    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error). mas não deixara o erro descrevido no detail da resposta
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar;
    """
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

@router.post("/login", 
             response_model=AuthResponse, 
             status_code=status.HTTP_201_CREATED)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_session)
) -> AuthResponse:
    """
    Endpoint com metodo POST, responsavel por realizar o login do usuário no sistema.

    O endpoint requer:
    - username (username ou email do usuário)
    - password (senha do usuário)

    caso esteja faltando algum dos campos obrigatorios, o endpoint irá retornar 422 (Unprocessable Entity).

    caso seja validado o usuário, o endpoint irá retornar um JSON contendo:
    - access_token: passe de curta duração usado para acessar recursos protegidos do sistema

    - refresh_token: passe de longa duração usado para obter um novo (access_token) sem o usuário ter que fazer login novamente

    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error). mas não deixara o erro descrevido no detail da resposta
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar;

    """
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
async def refresh_token(data: UserRefreshTokenSchema,
                        db: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """
    Endpoint com metodo POST, responsavel por realizar a criação de um novo (access_token) sem login.

    O endpoint requer:
    - refresh_token: passe de longa duração, recebido pelo Endpoint de (login)

    caso o (refresh_token) ja esteja expirado (passou o seu prazo de validade) ou esteja incorreto, será retornado um error 401 (Unauthorized).

    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error). mas não deixara o erro descrevido no detail da resposta
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar;
    """
    payload = verify_refresh_token(token=data.refresh_token)
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
    
