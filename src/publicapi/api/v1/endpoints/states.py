from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from typing import List, Optional

from publicapi.core.deps import get_current_user, get_session
from publicapi.models import StatesModel, UserModel
from publicapi.schemas.stateSchema import StatesSchemaBase

from publicapi.utils.querys_db import search_all_items_in_db, search_item_in_db

router = APIRouter()

@router.post("/", response_model=StatesSchemaBase, status_code=status.HTTP_201_CREATED)
async def create(data: StatesSchemaBase, 
                 db: AsyncSession = Depends(get_session),
                 user: UserModel = Depends(get_current_user)
) -> StatesSchemaBase:
    
    async with db as session:        
        new_state = StatesModel(
            name = data.name.title(),
            uf = data.uf.upper()
        )

        try:
            session.add(new_state)
            await session.commit()
            await session.refresh()
            return new_state
        
        except IntegrityError or UniqueViolationError:
            raise HTTPException(detail=f"Já existe uma instancia com o name:{new_state.name} e UF:{new_state.uf}", status_code=status.HTTP_409_CONFLICT)
        
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@router.get("/", response_model=List[StatesSchemaBase], status_code=status.HTTP_200_OK)
async def get(db: AsyncSession = Depends(get_session)):

    states: List[StatesSchemaBase] = await search_all_items_in_db(db=db,
                           Model=StatesModel)
    
    return states