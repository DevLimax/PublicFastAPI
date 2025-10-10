from fastapi import APIRouter, Depends, HTTPException, status, Query

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import CitiesModel, UserModel
from publicapi.schemas.citySchema import CitiesSchemaBase, CitiesSchemaCreate, CitiesSchemaWithRelations, CitiesFilters, CitiesSchemaResponse, CitiesSchemaWithRelationsResponse
from publicapi.schemas.ResponseSchema import NoAuthenticatedResponse, ConflictResponse, InternalServerResponse, NotFoundResponse

from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db
from publicapi.utils.exceptions import UniqueViolationException, ConflictException, NotFoundException


router = APIRouter()

@router.post("/", 
            summary="Criar Cidade",
            response_model=CitiesSchemaResponse, 
            status_code=status.HTTP_201_CREATED,
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "model": NoAuthenticatedResponse
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse
                },
                status.HTTP_409_CONFLICT: {
                    "model": ConflictResponse,
                }
             })
async def create(data: CitiesSchemaCreate,
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user),
):
    """
    Endpoint com metodo POST, responsavel por criar uma instancia na tabela (municipios).
    
    Para a criação de uma instancia (municipio), é necessario que o usuário esteja logado no sistema, e que o usuário tenha as permissoes de admin.
    caso não tenha permissoes de admin, o endpoint irá retornar 401 (Unauthorized).
    
    O endpoint requer id (codigo IBGE), name (nome da cidade) e state_id (id do estado ao qual pertence a cidade), somente o campo (id) é unico, mas os 
    campos (name e state_id) possuem Unique Constraint (não pode existir 2 cidades com o mesmo name e state_id), o endpoint irá retornar 409 (Conflict) 
    caso o (id) ou (name e state_id) seja igual a algum ja existente no banco de dados,
    caso esteja faltando algum desses campos, o endpoint irá retornar 422 (Unprocessable Entity).
    
    
    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error). mas não deixara o erro descrevido no detail da resposta
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar;
    """
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
            response_model=List[CitiesSchemaResponse], 
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                },
            }
)
async def get(db: AsyncSession = Depends(get_session),
              uf: str = Query(None, description="Sigla do estado ao qual pertence a cidade", examples=["SP", "CE", "MG"]),
              name: Optional[str] = Query(None, description="Nome da cidade")
):  
    """
    Endpoint com metodo GET, responsavel por listar todas as instancias na tabela (cidades).
    
    
    Não é necessario estar logado no sistema para utilizar o metodo GET desse endpoint.
    
    
    Esse endpoint possui filtros:
    - uf (sigla do estado ao qual pertence a cidade): ira listar todos os estados referente a (uf) inserida;
    - name (nome da cidade): ira listar todas as cidades refente ao (name) inserido.
    

    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error),
    mas não deixara o erro descrevido no detail da resposta.
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar.
    """
    
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
    Endpoint com metodo GET, responsavel por buscar uma instancia na tabela (cidades).    
    
    Não é necessario estar logado no sistema para utilizar o metodo GET desse endpoint
    
    O endpoint requer um ID como parametro, caso o ID seja inválido != int, o endpoint irá retornar 422 (Unprocessable Entity), 
    caso o id seja valido (int) mas não exista nenhuma instancia na tabela (estados) com o ID mencionado, 
    o endpoint irá retornar 404 (Not Found).
    
    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error),
    mas não deixara o erro descrevido no detail da resposta.
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar
    """
    
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



