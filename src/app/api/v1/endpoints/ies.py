from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.exceptions import ResponseValidationError
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import asyncpg

from app.core.deps import get_current_user, get_session
from app.models import IesModel, UserModel
from app.schemas.instituitionSchema import InstituitionSchemaBase, InstituitionSchemaCreate, IesFilters, InstituitionSchemaWithRelations, IesSchemaResponse, IesSchemaWithRelationsReponse
from app.schemas.ResponseSchema import NoAuthenticatedResponse, ConflictResponse, InternalServerResponse, NotFoundResponse

from app.utils.querys_db import search_all_items_in_db, search_item_in_db
from app.utils.exceptions import UniqueViolationException, UnauthorizedException

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
    if not user.is_admin:
        raise UnauthorizedException
    
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
            response_model=List[IesSchemaResponse], 
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                },
            }
)
async def get(
    db: AsyncSession = Depends(get_session),
    user: UserModel = Depends(get_current_user),
    abbreviation: Optional[str] = Query(
                                    None, 
                                    description="Sigla da instituição", 
                                    examples=['UFC', 'UFRJ', 'USP']
                                    ),
    type: Optional[str] = Query(
                            None,
                            description="Tipo da instituição", 
                            example='Federal'
                        ),
    uf: Optional[str] = Query(
                            None, 
                            description="Sigla do estado ao qual pertence a cidade onde encontra-se a instituição", 
                            examples=["SP", "CE", "MG"]
                        ),
    city_name: Optional[str] = Query(
                                   None, 
                                   description="Nome da cidade onde encontra-se a instituição"
                                ),
    city_code: Optional[int] = Query(
                                   None, 
                                   description="Código da cidade onde encontra-se a instituição"
                                )
):
    """
    Endpoint com metodo GET, responsavel por listar todas as instancias na tabela (instituições).
    
    
    Não é necessario estar logado no sistema para utilizar o metodo GET desse endpoint.
    
    
    Esse endpoint possui filtros:
    - abbreviation (Sigla da ies): Ira listar e retornar a instituição da qual a sigla pertence, o filtro tambem trará (Instituições) com siglas semelhantes;

    - type (tipo da faculdade: Federal, Municipal, Estadual): Ira listar todas as Instituições refente ao (type) inserido.

    - uf (Sigla do estado ao qual a faculdade pertence): Como toda faculdade pública pertence a um estado, foi disponibilizado o filtro por estado, usando
    a sigla do estado para uma melhor filtagrem.

    - city_name (nome da cidade): Caso hajá instituições que pertençam a uma cidade, será possivel filtrar essas IES com o nome da cidade
    a qual ela pertence.

    - city_code (id da cidade): Do mesmo jeito do city_name so que será necessario inserir o ID.

    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error),
    mas não deixara o erro descrevido no detail da resposta.
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar.
    """
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
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)                
):      
    """
    Endpoint com metodo GET, responsavel por buscar uma instancia na tabela (instituições).    
    
    Não é necessario estar logado no sistema para utilizar o metodo GET desse endpoint
    
    O endpoint requer um ID como parametro, caso o ID seja inválido != int, o endpoint irá retornar 422 (Unprocessable Entity), 
    caso o id seja valido (int) mas não exista nenhuma instancia na tabela (instituições) com o ID mencionado, 
    o endpoint irá retornar 404 (Not Found).
    
    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error),
    mas não deixara o erro descrevido no detail da resposta.
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar
    """
    ies = await search_item_in_db(id=id,
                                  Model=IesModel,   
                                  db=db
    )
    
    if not ies: 
        raise HTTPException(detail="Nenhuma instancia encontrada", status_code=status.HTTP_404_NOT_FOUND)
    return ies     