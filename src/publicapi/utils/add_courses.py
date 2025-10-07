from sqlalchemy.ext.asyncio import AsyncSession
from publicapi.core.db import Session
from publicapi.models import CourseLocationsModel
from publicapi.schemas.courseSchema import CourseLocationsSchemaCreate
import csv
import asyncio

async def add_course_locates_to_db():
    async with Session() as session:
        with open("src/Scripts/CSVs/courses_ies_extracted.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                course_instance = CourseLocationsSchemaCreate(
                    course_id = row.get('CODIGO_CURSO'),
                    city_id = row.get('CODIGO_MUNICIPIO'),
                    modality = row.get('MODALIDADE'),
                    situation = row.get('SITUACAO_CURSO'),
                    quantity_vacancies = row.get('QT_VAGAS_AUTORIZADAS'),
                    workload = row.get('CARGA_HORARIA')
                )
                try:
                    course = CourseLocationsModel(**course_instance.dict(exclude_unset=True))
                    session.add(course)
                    await session.commit()
                    await session.refresh(course)
                    print(f"Added successfully - Data: {course.__dict__}")
                
                except Exception as e:
                    print(f"Error: {str(e)}")
                    session.rollback()
                    continue

if __name__ == "__main__":
    asyncio.run(add_course_locates_to_db())