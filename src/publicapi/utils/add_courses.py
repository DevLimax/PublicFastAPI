from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from publicapi.core.db import Session
from publicapi.models import CourseLocationsModel, CoursesModel, CitiesModel
from publicapi.schemas.courseSchema import CourseLocationsSchemaCreate
import csv
import asyncio
from colorama import Fore, init

init(autoreset=True)

async def add_course_locates_to_db():
    async with Session() as session:
        with open("src/Scripts/CSVs/courses_ies_extracted.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                course = await session.get(CoursesModel, int(row.get("CODIGO_CURSO")))
                city = await session.get(CitiesModel, int(row.get("CODIGO_MUNICIPIO")))
                
                if city and course:
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
                        print(f"{Fore.GREEN}Added successfully {Fore.WHITE}Course:{Fore.CYAN}{course_instance.course_id}{Fore.WHITE} to city:{Fore.CYAN}{course_instance.city_id}")
                    
                    except IntegrityError as e:
                        await session.rollback()
                        e_str = str(e).lower()
                        if "unique constraint" in e_str:
                            print(f"{Fore.RED}Error: {Fore.YELLOW}Course {row.get('CODIGO_CURSO')} already exists in city {row.get('CODIGO_MUNICIPIO')}")
                        else:
                            print(f"{Fore.RED}Error: {Fore.YELLOW}{str(e)}")    
                        
                    
                    except Exception as e:
                        print(f"{Fore.RED}Error: {Fore.YELLOW}{str(e)}")
                        session.rollback()
                        continue
                    
                if not course:
                    print(f"{Fore.RED}Error: {Fore.YELLOW}Course {row.get('CODIGO_CURSO')} not found")
                                
                if not city:
                    print(f"{Fore.RED}Error: {Fore.YELLOW}City {row.get('CODIGO_MUNICIPIO')} not found")
                    
                    
if __name__ == "__main__":
    asyncio.run(add_course_locates_to_db())