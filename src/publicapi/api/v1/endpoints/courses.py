from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import CoursesModel, UserModel
from publicapi.schemas.courseSchema import CourseSchemaBase, CourseFilters, CourseSchemaCreate, CourseWithRelations

from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db

router = APIRouter()

@router.post("/", 
            summary="Criar Curso",
            description="Retorna uma instancia criada no DB, apartir do corpo JSON enviado",
            response_model=CourseSchemaBase, 
            status_code=status.HTTP_201_CREATED)
async def create(data: CourseSchemaCreate, 
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)
):
    
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
            description="Retorna uma lista de cursos. Suporta filtragem por (name, academic_degree, ies_id) filtros tipo String suportam (ilike)",
            response_model=List[CourseSchemaBase], 
            status_code=status.HTTP_200_OK
)
async def get(db: AsyncSession = Depends(get_session),
              name: Optional[str] = Query(None, description="Nome do curso"),
              academic_degree: Optional[str] = Query(None, description="Grau acadêmico do curso", examples=["Bacharelado", "Licenciatura"]),
              ies_id: Optional[int] = Query(None, description="ID (codigo) da Instituição de ensino")
):
    
    filters: CourseFilters = CourseFilters(name=name, academic_degree=academic_degree, ies_id=ies_id)
    courses = await search_all_items_in_db(db=db,
                                     Model=CoursesModel,
                                     filters=filters
    )
    return courses

@router.get("/{id}", 
            summary="Buscar Curso por ID",
            description="Retorna uma instancia filtrada por ID. caso não exista nenhuma instancia na tabela (cursos) com o ID mencionado, sera retornado 404",
            response_model=CourseWithRelations, 
            status_code=status.HTTP_200_OK
)
async def get_id(id: int, 
                 db: AsyncSession = Depends(get_session)
):
    
    course = await search_item_in_db(id=id,
                               db=db,
                               Model=CoursesModel)
    
    if not course: 
        raise HTTPException(detail=f"Curso não encontrado para o id: {id}", status_code=status.HTTP_404_NOT_FOUND)
    
    return course
