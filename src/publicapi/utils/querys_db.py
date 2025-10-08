
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta, aliased, contains_eager, selectinload, joinedload
from sqlalchemy import exists, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from publicapi.core.configs import settings
from publicapi.models import *
from typing import Optional, Type

async def search_item_in_db(id: int, 
                            Model: Type[DeclarativeMeta], 
                            db: AsyncSession,
):
    """
    Função para buscar um item no banco de dados pelo ID.
    """ 
    query = select(Model).filter(Model.id == id )
    if Model == CitiesModel:
        query = query.options(
            joinedload(CitiesModel.state),
            joinedload(CitiesModel.instituitions)
        )
    
    if Model == StatesModel:
        query = query.options(
            joinedload(StatesModel.cities),
            joinedload(StatesModel.instituitions)
        )
    
    if Model == IesModel:
        query = query.options(
            joinedload(IesModel.state),
            joinedload(IesModel.city),
            joinedload(IesModel.courses)
        )
        
    if Model == CoursesModel:
        query = query.options(
            joinedload(CoursesModel.ies).options(
                joinedload(IesModel.state),
                joinedload(IesModel.city)
            ),
            joinedload(CoursesModel.locations).options(
                joinedload(CourseLocationsModel.city)
            )
        )
    
    result = await db.execute(query)
    item = result.scalars().unique().one_or_none()
    return item

async def search_all_items_in_db(Model: Type[DeclarativeMeta],
                                 db: AsyncSession,
                                 filters: Optional[dict] = None,
                                 skip: int = 0,
                                 limit: int = None
):
    query = select(Model).order_by(Model.id)
    if Model == CitiesModel:
        query = query.options(
            selectinload(CitiesModel.state),
            selectinload(CitiesModel.instituitions)
        )
    
    if Model == StatesModel:
        query = query.options(
            selectinload(StatesModel.instituitions).options(
                selectinload(IesModel.city),
                selectinload(IesModel.state)
            )
        )
    
    if Model == IesModel:
        query = query.options(
            selectinload(IesModel.state),
            selectinload(IesModel.city),
            selectinload(IesModel.courses)
        )
    
    if Model == CoursesModel:
        query = query.options(
            selectinload(CoursesModel.ies).options(
                selectinload(IesModel.state),
                selectinload(IesModel.city)
            ),
        )
    
    if filters:            
        if Model == CitiesModel and filters.uf:
            query = query.join(CitiesModel.state)
            query = query.where(StatesModel.uf.ilike(f"%{filters.uf}%")) 
            query = query.distinct()
            
        if Model == IesModel and (filters.city_name or filters.city_code or filters.uf):
            query = query.join(IesModel.state)
            query = query.join(IesModel.city)
            if filters.city_name:
                query = query.where(CitiesModel.name.ilike(f"%{filters.city_name}%"))
            if filters.city_code:
                query = query.where(CitiesModel.id == filters.city_code)
            if filters.uf:
                query = query.where(StatesModel.uf.ilike(f"%{filters.uf}%")) 
        
        for atrr, value in filters.dict(exclude_none=True).items():
            try: 
                column = getattr(Model, atrr)
            except AttributeError:
                continue
                
            if column is not None:
                if isinstance(value, str):
                    if atrr == "type":
                        query = query.filter(cast(column, String).ilike(f"%{value}%"))
                    elif atrr == "academic_degree":
                        query = query.where(cast(column, String).ilike(f"%{value}%"))
                    else:
                        query = query.where(column.ilike(f"%{value}%"))
                else:
                    query = query.where(column == value)
                        
        query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    list_items = result.scalars().unique().all()
    return list_items
