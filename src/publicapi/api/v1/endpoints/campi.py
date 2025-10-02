from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import UserModel, CampiModel
from publicapi.schemas.campiSchemas import CampiSchemaBase, CampiSchemaCreate

from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db


router = APIRouter()

@router.post("/", response_model=CampiSchemaBase, status_code=status.HTTP_201_CREATED)
async def create(data: CampiSchemaCreate,
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)
):
    
    async with db as session:
        new_campus = CampiModel(
            id = data.id,
            name = data.name,
            ies_id = data.ies_id,
            state_id = data.state_id,
            city_id = data.city_id,
            district = data.district,
            cep = data.cep,
            street = data.street,
            number = data.number,
            email = data.email,
            telephone = data.telephone
        )
        try:
            new_campus.validate_data()
            session.add(new_campus)
            await session.commit()
            await session.refresh(new_campus)
            return await search_item_in_db(id=new_campus.id, Model=CampiModel, db=db)

        except ValueError as e:
            msg = str(e)
            raise HTTPException(detail=msg, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
        
        except IntegrityError as e:
            raise HTTPException(detail=f"Ja existe uma instancia com as colunas inseridas", status_code=status.HTTP_409_CONFLICT)

        except Exception as e:
            raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@router.get("/", response_model=List[CampiSchemaBase], status_code=status.HTTP_200_OK)
async def get(db: AsyncSession = Depends(get_session)):
    
    campi = await search_all_items_in_db(db=db,
                                         Model=CampiModel)
    return campi


@router.get("/{id}", response_model=CampiSchemaBase, status_code=status.HTTP_200_OK)
async def get_id(id: int,
                 db: AsyncSession = Depends(get_session)
):
    
    campus = await search_item_in_db(id=id,
                                     Model=CampiModel,
                                     db=db
    )
    
    if not campus:
        raise HTTPException(detail="Nenhuma instancia encontrada", status_code=status.HTTP_404_NOT_FOUND)
    
    return campus 