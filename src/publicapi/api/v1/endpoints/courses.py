from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import CoursesModel, UserModel
from publicapi.schemas.courseSchema import CourseSchemaBase, CourseFilters, CourseSchemaCreate, CourseWithRelations, CourseSchemaResponse, CourseSchemaWithRelationsResponse
from publicapi.schemas.ResponseSchema import NoAuthenticatedResponse, ConflictResponse, InternalServerResponse, NotFoundResponse

from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db

router = APIRouter()

@router.post("/", 
            summary="Criar Curso",
            response_model=CourseSchemaResponse, 
            status_code=status.HTTP_201_CREATED,
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "model": NoAuthenticatedResponse, 
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                },
                status.HTTP_409_CONFLICT: {
                    "model": ConflictResponse,
                }
            }
)

async def create(data: CourseSchemaCreate, 
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)
):
    """
    Endpoint com metodo POST, responsavel por criar uma instancia na tabela (cursos).
    
    Para a criação de uma instancia (curso), é necessario que o usuário esteja logado no sistema, e que o usuário tenha as permissoes de admin.
    caso não tenha permissoes de admin, o endpoint irá retornar 401 (Unauthorized).
    
    O endpoint requer:
    - id (codigo do curso cadastrado no mec) (Unico)
    - name (nome do curso)
    - area_ocde (área do saber à qual um curso pertence) -> opcional 
    - ies_id (ID da instituição) (FK)
    - academic_degree: (grau acadêmico do curso)

    Relações do banco:
    - ies (instituição ao qual o curso pertence): após criar uma instancia de curso, o ies_id irá relacionar com a instancia de (instituições) da qual o ID pertence.

    - locations (locais onde o curso está disponivel): essa é uma relação one-to-many, onde um curso pode ter varios locais de disponibilidade, e em cada
    local vai ter dados complementares como: (workload, modality, situation, quantity_vacancies, city)
    
    Nessa tabela não existe Unique Constraint, mas caso ja exista um curso com mesmo (id) o endpoint irá retornar 409 (Conflict)
    
    caso esteja faltando algum dos campos obrigatorios, o endpoint irá retornar 422 (Unprocessable Entity).
    

    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error). mas não deixara o erro descrevido no detail da resposta
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar;
    """
    async with db as session:

        course = CoursesModel(
            id = data.id,
            name = data.name,
            area_ocde = data.area_ocde,
            ies_id = data.ies_id,
            academic_degree = data.academic_degree,
        )

        try:
            course.validate_data()
            session.add(course)
            await session.commit()
            await session.refresh(course)
            return await search_item_in_db(id=course.id, Model=CoursesModel, db=db)
        
        except ValueError as e:
            msg = str(e)
            raise HTTPException(detail=msg, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
        
        except IntegrityError as e:
            raise HTTPException(detail=str(e), status_code=status.HTTP_409_CONFLICT)

        except Exception as e:
            msg = str(e)
            raise HTTPException(detail=f"Erro interno do servidor: {msg}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@router.get("/", 
            summary="Listar e Filtrar Cursos",
            response_model=List[CourseSchemaResponse], 
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "model": InternalServerResponse,
                }
            }
)
async def get(db: AsyncSession = Depends(get_session),
              name: Optional[str] = Query(None, description="Nome do curso"),
              academic_degree: Optional[str] = Query(None, description="Grau acadêmico do curso", examples=["Bacharelado", "Licenciatura"]),
              ies_id: Optional[int] = Query(None, description="ID (codigo) da Instituição de ensino")
):
    """
    Endpoint com metodo GET, responsavel por listar todas as instancias na tabela (cursos).
    
    
    Não é necessario estar logado no sistema para utilizar o metodo GET desse endpoint.
    
    
    Esse endpoint possui filtros:
    - name (Nome do curso): Ira listar e retornar os cursos que possuem o nome inserido

    - academic_degree (Grau acadêmico): Ira listar todos os cursos refente ao (academic_degree) inserido.

    - ies_id (ID da instituição ao qual o curso pertence): Como todo curso pertence a uma instituição, foi disponibilizado o filtro por instituição, usando
    o codigo da instituição para uma melhor filtagrem.

    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error),
    mas não deixara o erro descrevido no detail da resposta.
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar.
    """

    filters: CourseFilters = CourseFilters(name=name, academic_degree=academic_degree, ies_id=ies_id)
    courses = await search_all_items_in_db(db=db,
                                     Model=CoursesModel,
                                     filters=filters
    )
    return courses

@router.get("/{id}", 
            summary="Buscar Curso por ID",
            response_model=CourseSchemaWithRelationsResponse, 
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
    Endpoint com metodo GET, responsavel por buscar uma instancia na tabela (cursos).    
    
    Não é necessario estar logado no sistema para utilizar o metodo GET desse endpoint

    
    O endpoint requer um ID como parametro, caso o ID seja inválido != int, o endpoint irá retornar 422 (Unprocessable Entity), 
    caso o id seja valido (int) mas não exista nenhuma instancia na tabela (instituições) com o ID mencionado, 
    o endpoint irá retornar 404 (Not Found).
    
    Caso aconteça algum erro inesperado no servidor, o endpoint irá retornar 500 (Internal Server Error),
    mas não deixara o erro descrevido no detail da resposta.
    o erro irá aparecer no log do servidor para o desenvolvedor conseguir validar o problema e solucionar
    """
    course = await search_item_in_db(id=id,
                               db=db,
                               Model=CoursesModel)
    
    if not course: 
        raise HTTPException(detail=f"Curso não encontrado para o id: {id}", status_code=status.HTTP_404_NOT_FOUND)
    
    return course
