from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.exceptions import ResponseValidationError
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import asyncpg

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import IesModel, UserModel
from publicapi.schemas.instituitionSchema import InstituitionSchemaBase, InstituitionSchemaCreate, IesFilters, InstituitionSchemaWithRelations, IesSchemaResponse, IesSchemaWithRelationsReponse
from publicapi.schemas.ResponseSchema import NoAuthenticatedResponse, ConflictResponse, InternalServerResponse, NotFoundResponse

from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db
from publicapi.utils.exceptions import UniqueViolationException

router = APIRouter()

@router.post("/", 
             summary="Criar Instituição",
             response_model=IesSchemaResponse, 
             status_code=status.HTTP_201_CREATED,
             responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "model": NoAuthenticatedResponse, 
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                },
                status.HTTP_409_CONFLICT: {
                    "model": ConflictResponse
                }
             }
)
async def create(data: InstituitionSchemaCreate, 
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)
):
    """
    Endpoint com metodo POST, responsavel por criar uma instancia na tabela (instituições).
    
    Para a criação de uma instancia (instituição), é necessario que o usuário esteja logado no sistema, e que o usuário tenha as permissoes de admin.
    caso não tenha permissoes de admin, o endpoint irá retornar 401 (Unauthorized).
    
    O endpoint requer:
    - id (codigo da ies cadastrada no mec) (Unico)
    - name (nome da instituição) (Unico)
    - abbreviation (sigla da instituição) -> opcional (Unico)
    - type (tipo da instituição)
    - site (site da instituição) -> opcional
    - state_id (id do estado ao qual pertence a instituição)
    - city_id (id da cidade ao qual pertence a instituição) -> opcional
    
    Nessa tabela não existe Unique Constraint, mas caso ja exista uma ies com mesmo (id, name ou abbreviation) o endpoint irá retornar 409 (Conflict)
    
    caso esteja faltando algum dos campos obrigatorios, o endpoint irá retornar 422 (Unprocessable Entity).
    
    
    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error). mas não deixara o erro descrevido no detail da resposta
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar;
    """
    async with db as session:
        new_ies = IesModel(
            id = data.id,
            name = data.name,
            abbreviation = data.abbreviation if data.abbreviation != "" else None,
            state_id = data.state_id,
            city_id = data.city_id,
            type = data.type,
            site = data.site if data.site != "" else None
        )
        
        try:
            new_ies.validate_data()
            session.add(new_ies)
            await session.commit()
            await session.refresh(new_ies)
            return await search_item_in_db(id=new_ies.id, Model=IesModel, db=db)
        
        except ResponseValidationError as e:
            await session.rollback()
            raise HTTPException(detail=str(e), status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
           
        except ValueError as e:
            await session.rollback()
            raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(detail="Já existe uma instancia com os dados inseridos.", status_code=status.HTTP_409_CONFLICT)
        
        except Exception as e:
            await session.rollback()
            raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/",
            summary="Listar e Filtrar Instituições",
            description="Retorna uma lista de instituições. Suporta filtragem por (abbreviation, type, uf, city_name e city_code) filtros tipo String suportam (ilike)", 
            response_model=List[IesSchemaResponse], 
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                },
            }
)
async def get(db: AsyncSession = Depends(get_session),
              abbreviation: Optional[str] = Query(None, 
                                        description="Sigla da instituição", 
                                        examples=['UFC', 'UFRJ', 'USP']),
              type: Optional[str] = Query(None,
                                                           description="Tipo da instituição", 
                                                           example='Federal'),
              uf: Optional[str] = Query(None, 
                                        description="Sigla do estado ao qual pertence a cidade onde encontra-se a instituição", 
                                        examples=["SP", "CE", "MG"]),
              city_name: Optional[str] = Query(None, 
                                               description="Nome da cidade onde encontra-se a instituição"),
              city_code: Optional[int] = Query(None, 
                                               description="Código da cidade onde encontra-se a instituição")
):
    filters: IesFilters = IesFilters(abbreviation=abbreviation, 
                                     type=type.capitalize() if type else None, 
                                     uf=uf, city_name=city_name, 
                                     city_code=city_code
    )
    instituitions = await search_all_items_in_db(db=db,
                                       Model=IesModel,
                                       filters=filters
    )
    return instituitions


@router.get("/{id}",
            summary="Buscar Instituição por ID",
            description="Retorna uma instancia com suas relações filtrada por ID. caso não exista nenhuma instancia na tabela (instituicoes) com o ID mencionado, sera retornado 404", 
            response_model=IesSchemaWithRelationsReponse, 
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                },
                status.HTTP_404_NOT_FOUND:{
                    "model": NotFoundResponse,
                }
            }
)
async def get_id(id: int,
                 db: AsyncSession = Depends(get_session)                 
):      
    
    ies = await search_item_in_db(id=id,
                                  Model=IesModel,   
                                  db=db
    )
    
    if not ies: 
        raise HTTPException(detail="Nenhuma instancia encontrada", status_code=status.HTTP_404_NOT_FOUND)
    return ies     