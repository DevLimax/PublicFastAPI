from fastapi import APIRouter, Depends, HTTPException, status, Query

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from typing import List, Optional, Union

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import StatesModel, UserModel
from publicapi.schemas.stateSchema import StatesSchemaBase, StatesSchemaResponse, StatesSchemaWithRelations, StatesSchemaWithRelationsResponse, StateFilters
from publicapi.schemas.ResponseSchema import NoAuthenticatedResponse, InternalServerResponse, ConflictResponse, NotFoundResponse

from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db
from publicapi.utils.exceptions import ConflictException, UniqueViolationException, InternalServerException, NotFoundException

router = APIRouter()

@router.post("/", 
             summary="Criar Estado",
             response_model=StatesSchemaResponse, 
             status_code=status.HTTP_201_CREATED,
             responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "model": NoAuthenticatedResponse
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse
                },
                status.HTTP_409_CONFLICT: {
                    "model": ConflictResponse
                }
             }    
            )
async def create(data: StatesSchemaBase, 
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)
):
    """
    Endpoint com metodo POST, responsavel por criar uma instancia na tabela (estados).
    
    Para a criação de uma instancia (estado), é necessario que o usuário esteja logado no sistema, e que o usuário tenha as permissoes de admin.
    caso não tenha permissoes de admin, o endpoint irá retornar 401 (Unauthorized).
    
    
    O endpoint requer somente o nome (name) e a sigla do estado (uf), o ID é gerado de forma automatica, se caso o usuário tente adicionar
    um estado com nome ou uf ja existente no banco, o endpoint irá retornar 409 (Conflict), ja que todo estado tem seu nome e uf unicos, caso esteja faltando
    algum desses campos, o endpoint irá retornar 422 (Unprocessable Entity).
    
    
    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error). mas não deixara o erro descrevido no detail da resposta
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar;
    """
    async with db as session:        
        new_state = StatesModel(
            name = data.name.title(),
            uf = data.uf.upper()
        )
        try:
            session.add(new_state)
            await session.commit()
            await session.refresh(new_state)
            return await search_item_in_db(id=new_state.id, Model=StatesModel, db=db)
        
        except IntegrityError as e:
            e_str = str(e.orig).lower()
            if "uniqueviolationerror" in e_str:
                if "uf" in e_str:
                    raise UniqueViolationException(field='uf', value=data.uf)
                elif "name" in e_str:
                    raise UniqueViolationException(field='name', value=data.name)
                else:
                    raise UniqueViolationException(field='id', value=new_state.id)
        
        except Exception as e:
            raise InternalServerException()
        
@router.get("/", 
            summary="Listar e Filtrar Estados",
            response_model=List[Union[StatesSchemaResponse]], 
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse
                },
            }
)
async def get(db: AsyncSession = Depends(get_session),
              uf: Optional[str] = Query(None, description="Sigla do estado", examples=["SP", "CE", "MG"])
):  
    """
    Endpoint com metodo GET, responsavel por listar todas as instancias na tabela (estados).
    
    Não é necessario estar logado no sistema para utilizar o metodo GET desse endpoint, esse endpoint possui
    apenas um filtro (uf) que permite o usuário filtrar as instancias por sigla de estado.
    

    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error),
    mas não deixara o erro descrevido no detail da resposta.
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar;
    """
    
    try:
        filters: StateFilters = StateFilters(uf=uf)
        states = await search_all_items_in_db(db=db,
                                            Model=StatesModel,
                                            filters=filters
        )
        return states
    except Exception as e:
        print(e)
        raise InternalServerException()

@router.get("/{id}", 
            summary="Buscar Estado por ID",
            response_model=StatesSchemaWithRelationsResponse, 
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse
                },
                status.HTTP_404_NOT_FOUND:{
                    "model": NotFoundResponse
                }
            }
)
async def get_id(id: int,
                 db: AsyncSession = Depends(get_session)
):
    """
    Endpoint com metodo GET, responsavel por buscar uma instancia na tabela (estados).    
    
    Não é necessario estar logado no sistema para utilizar o metodo GET desse endpoint
    
    O endpoint requer um ID como parametro, caso o ID seja inválido != int, o endpoint irá retornar 422 (Unprocessable Entity), caso o id seja valido (int)
    mas não exista nenhuma instancia na tabela (estados) com o ID mencionado, o endpoint irá retornar 404 (Not Found).
    
    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error),
    mas não deixara o erro descrevido no detail da resposta.
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar
    """
    try:
        state = await search_item_in_db(id=id,
                                        Model=StatesModel,
                                        db=db
        )
    except Exception as e:
        print(e)
        InternalServerException()

    if not state:
        raise NotFoundException(id=id)
    
    return state

