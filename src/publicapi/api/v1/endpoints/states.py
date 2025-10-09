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
             description="Retorna uma instancia criada no DB, apartir do corpo JSON enviado",
             response_model=StatesSchemaResponse, 
             status_code=status.HTTP_201_CREATED,
             response_description="Resposta bem-sucedida",
             responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "model": NoAuthenticatedResponse, 
                    "description": "Erro de autenticação"
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                    "description": "Erro interno do servidor"
                },
                status.HTTP_409_CONFLICT: {
                    "model": ConflictResponse,
                    "description": "Erro de conflito"
                }
             }    
            )
async def create(data: StatesSchemaBase, 
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)
):
    
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
            description="Retorna uma lista de estados brasileiros. Suporta filtragem por UF(Codigo IBGE) (ilike)",
            response_model=List[Union[StatesSchemaResponse, StatesSchemaWithRelationsResponse]], 
            response_description="Resposta bem-sucedida",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                    "description": "Erro interno do servidor"
                },
            }
)
async def get(db: AsyncSession = Depends(get_session),
              uf: Optional[str] = Query(None, description="Sigla do estado", examples=["SP", "CE", "MG"])
):  
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
            description="Retorna uma instancia filtrada por ID. caso não exista nenhuma instancia na tabela (estados) com o ID mencionado, sera retornado 404",
            response_model=StatesSchemaWithRelationsResponse, 
            response_description="Resposta bem-sucedida",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                    "description": "Erro interno do servidor"
                },
                status.HTTP_404_NOT_FOUND:{
                    "model": NotFoundResponse,
                    "description": "Instancia não encontrada"
                }
            }
)
async def get_id(id: int,
                 db: AsyncSession = Depends(get_session)
):
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

