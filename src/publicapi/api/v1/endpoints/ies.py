from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import ResponseValidationError
from typing import List, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import asyncpg

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import IesModel, UserModel
from publicapi.schemas.instituitionSchema import InstituitionSchemaBase, InstituitionSchemaCreate, IesFilters, InstituitionSchemaWithRelations
from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db
from publicapi.utils.exceptions import UniqueViolationException

router = APIRouter()

@router.post("/", response_model=InstituitionSchemaBase, status_code=status.HTTP_201_CREATED)
async def create(data: InstituitionSchemaCreate, 
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)
):
    
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


@router.get("/", response_model=List[InstituitionSchemaBase], status_code=status.HTTP_200_OK)
async def get(db: AsyncSession = Depends(get_session),
              filters: IesFilters = Depends()
):
    
    instituitions = await search_all_items_in_db(db=db,
                                       Model=IesModel,
                                       filters=filters
    )
    return instituitions


@router.get("/{id}", response_model=InstituitionSchemaWithRelations, status_code=status.HTTP_200_OK)
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