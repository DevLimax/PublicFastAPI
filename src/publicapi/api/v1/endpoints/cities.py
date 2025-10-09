from fastapi import APIRouter, Depends, HTTPException, status, Query

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import CitiesModel, UserModel
from publicapi.schemas.citySchema import CitiesSchemaBase, CitiesSchemaCreate, CitiesSchemaWithRelations, CitiesFilters
from publicapi.schemas.ResponseSchema import NoAuthenticatedResponse, ConflictResponse, InternalServerResponse, NotFoundResponse

from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db
from publicapi.utils.exceptions import UniqueViolationException, ConflictException, NotFoundException


router = APIRouter()

@router.post("/", 
            summary="Criar Cidade",
            description="Retorna uma instancia criada no DB, apartir do corpo JSON enviado",
            response_model=CitiesSchemaBase, 
            response_description="Resposta bem-sucedida",
            status_code=status.HTTP_201_CREATED,
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
             })
async def create(data: CitiesSchemaCreate,
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user),
):
    
    async with db as session:
        new_city = CitiesModel(
            id = data.id,
            name = data.name.title(),
            state_id = data.state_id
        )
        
        try: 
            session.add(new_city)
            await session.commit()
            await session.refresh(new_city)
            return await search_item_in_db(id=new_city.id, Model=CitiesModel, db=db) 
        
        except IntegrityError as e:
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise UniqueViolationException(field="id", value=data.id)
            else:
                raise HTTPException(detail="Error de conflito", status_code=status.HTTP_409_CONFLICT)
        except Exception as e:
            raise InternalServerResponse()

@router.get("/", 
            summary="Listar e Filtrar Cidades",
            description="Retorna uma lista de cidades brasileiras. Suporta filtragem por (uf, name) ambos (ilike)",
            response_model=List[CitiesSchemaBase], 
            response_description="Resposta bem-sucedida",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                    "description": "Erro interno do servidor"
                }
            })
async def get(db: AsyncSession = Depends(get_session),
              uf: str = Query(None, description="Sigla do estado ao qual pertence a cidade", examples=["SP", "CE", "MG"]),
              name: Optional[str] = Query(None, description="Nome da cidade")
):  
    try:
        filters: CitiesFilters = CitiesFilters(uf=uf, name=name)
        cities = await search_all_items_in_db(db=db, 
                                            Model=CitiesModel, 
                                            filters=filters
        )
        return cities
    except Exception as e:
        print(e)
        raise InternalServerResponse()

@router.get("/{id}", 
            summary="Buscar Cidade por ID",
            description="Retorna uma instancia com suas relações filtrada por ID. caso não exista nenhuma instancia na tabela (cidades) com o ID mencionado, sera retornado 404",
            response_model=CitiesSchemaWithRelations, 
            response_description="Resposta bem-sucedida",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                    "description": "Erro interno do servidor"
                },
                status.HTTP_404_NOT_FOUND: {
                    "model": NotFoundResponse,
                    "description": "Instancia não encontrada"
                }
            }
)
async def get_id(id: int,
                 db: AsyncSession = Depends(get_session)
):
    try:
        citie = await search_item_in_db(id=id,
                                        Model=CitiesModel,
                                        db=db
        )
    except Exception as e:
        print(e)
        raise InternalServerResponse()

    if not citie:
        raise NotFoundException(id=id)
    
    return citie



