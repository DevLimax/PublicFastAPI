
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta, aliased, contains_eager
from sqlalchemy import exists, cast
from sqlalchemy.ext.asyncio import AsyncSession
from publicapi.core.configs import settings
from publicapi.models import CitiesModel, StatesModel, IesModel
from typing import Optional, Type

async def search_item_in_db(id: int, 
                            Model: Type[DeclarativeMeta], 
                            db: AsyncSession,
):
    """
    Função para buscar um item no banco de dados pelo ID.
    """ 
    query = select(Model).filter(Model.id == id )
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

    if filters:
        
        if Model == StatesModel and (filters.city_name or filters.city_code):
            cityAlias = aliased(CitiesModel)

            query = query.join(cityAlias ,Model.cities)
        
            if filters.city_name:
                query = query.where(cityAlias.name.ilike(f"%{filters.city_name}%"))
            if filters.city_code:
                query = query.where(cityAlias.id == filters.city_code)
            
            query = query.options(contains_eager(Model.cities, alias=cityAlias))
            query = query.distinct()
           
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
                if isinstance(value, str) and (atrr != "type" and atrr != "academic_degree"):
                    query = query.where(column.ilike(f"%{value}%"))
                else:
                    query = query.where(column == value)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    list_items = result.scalars().unique().all()
    return list_items
