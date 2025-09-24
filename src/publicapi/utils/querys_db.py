
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from publicapi.core.configs import settings
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
        for atrr, value in filters.dict(exclude_none=True).items():
            try: 
                column = getattr(Model, atrr)
            except AttributeError:
                continue
            
            if column is not None:
                if isinstance(value, str):
                    query = query.where(column.ilike(f"%{value}%"))
                else:
                    query = query.where(column == value)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    list_items = result.scalars().unique().all()
    return list_items
