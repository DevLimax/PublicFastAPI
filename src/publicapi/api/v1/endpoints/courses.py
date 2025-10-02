from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import CoursesModel, UserModel
from publicapi.schemas.courseSchema import CourseSchemaBase, CourseFilters

from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db

router = APIRouter()

@router.post("/", response_model=CourseSchemaBase, status_code=status.HTTP_201_CREATED)
async def create(data: CourseSchemaBase, 
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)
):
    
    async with db as session:

        course = CoursesModel(
            name = data.name,
            area_ocde = data.area_ocde,
            workload = data.workload,
            academic_degree = data.academic_degree
        )
        course.validate_data()

        try:
            session.add(course)
            await session.commit()
            await session.refresh(course)
            return await search_item_in_db(id=course.id, Model=CoursesModel, db=db)
        
        except ValueError as e:
            msg = str(e)
            raise HTTPException(detail=msg, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
        
        except IntegrityError as e:
            raise HTTPException(detail=f"Ja existe uma instancia com a coluna (name) = ({course.name})", status_code=status.HTTP_409_CONFLICT)

        except Exception as e:
            msg = str(e)
            raise HTTPException(detail=f"Erro interno do servidor: {msg}", status_code=status.http_500)
        
@router.get("/", response_model=List[CourseSchemaBase], status_code=status.HTTP_200_OK)
async def get(db: AsyncSession = Depends(get_session),
              filters: CourseFilters = Depends()
):

    courses = await search_all_items_in_db(db=db,
                                     Model=CoursesModel,
                                     filters=filters
    )
    return courses

@router.get("/{id}", response_model=CourseSchemaBase, status_code=status.HTTP_200_OK)
async def get_id(id: int, 
                 db: AsyncSession = Depends(get_session)
):
    
    course = await search_item_in_db(id=id,
                               db=db,
                               Model=CoursesModel)
    
    if not course: 
        raise HTTPException(detail=f"Curso não encontrado para o id: {id}", status_code=status.HTTP_404_NOT_FOUND)
    
    return course
