from fastapi import APIRouter, Depends, HTTPException, status, Query

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import CitiesModel, UserModel
from publicapi.schemas.citySchema import CitiesSchemaBase, CitiesSchemaCreate, CitiesSchemaWithRelations, CitiesFilters

from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db


router = APIRouter()

@router.post("/", response_model=CitiesSchemaBase, status_code=status.HTTP_201_CREATED)
async def create(data: CitiesSchemaCreate,
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)
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
        
        except (IntegrityError, UniqueViolationError):
            raise HTTPException(detail=f"Já existe uma instancia com o id:{new_city.id}", status_code=status.HTTP_409_CONFLICT)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/", response_model=List[CitiesSchemaBase], status_code=status.HTTP_200_OK)
async def get(db: AsyncSession = Depends(get_session),
              uf: str = Query(None, description="Sigla do estado ao qual pertence a cidade", examples=["SP", "CE", "MG"]),
              name: Optional[str] = Query(None, description="Nome da cidade")
):  
    filters: CitiesFilters = CitiesFilters(uf=uf, name=name)
    cities = await search_all_items_in_db(db=db, 
                                          Model=CitiesModel, 
                                          filters=filters
    )
    return cities

@router.get("/{id}", response_model=CitiesSchemaWithRelations, status_code=status.HTTP_200_OK)
async def get_id(id: int,
                 db: AsyncSession = Depends(get_session)
):
    
    citie = await search_item_in_db(id=id,
                                    Model=CitiesModel,
                                    db=db
    )
    
    if not citie:
        raise HTTPException(detail="Nenhuma instancia encontrada", status_code=status.HTTP_404_NOT_FOUND)
    return citie
