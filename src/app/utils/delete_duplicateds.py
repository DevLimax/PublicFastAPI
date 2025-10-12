from app.core.db import Session
from app.models import CourseLocationsModel
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta
from typing import List, Type
import asyncio

async def delete_duplicateds(Model: Type[DeclarativeMeta]):    
    async with Session() as session:
        query = select(Model).order_by(Model.id)
        result = await session.execute(query)
        items: List[Model] = result.scalars().all()
        uniques = set()
        list_to_delete = []
        
        for item in items:
            key = (item.course_id, item.city_id)
            
            if key not in uniques:
                uniques.add(key)
            
            else:
                print("Um item foi adicionado a lista de duplicados")
                list_to_delete.append(item)
            
        for item in list_to_delete:
            await session.delete(item)
            await session.commit()
            print(f"Item deletado: {item.id} - {item.course_id} - {item.city_id}")
            
            
            

if __name__ == "__main__":
    asyncio.run(delete_duplicateds(Model=...))

        
        