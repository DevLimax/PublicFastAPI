import csv
import asyncio
from colorama import init, Fore
from publicapi.core.db import Session
from publicapi.models import CoursesModel
from publicapi.schemas.courseSchema import CourseSchemaCreate

filepath: str = "src/Scripts/CSVs/courses_ies_extracted.csv"
lines_with_error: list = []
init(autoreset=True)

async def add_cursos():
    async with Session() as session:
        with open(filepath, "r", encoding="utf-8",) as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                if row["GRAU"] == "Tecnológico":
                    row["GRAU"] = "Tecnologo"
            
                elif row["GRAU"] == "Área Básica de Ingresso (ABI)":
                    row["GRAU"] = "ABI"
                
                course_instance = CourseSchemaCreate(
                        id = row.get('CODIGO_CURSO'),
                        name = row.get('NOME_CURSO'),
                        area_ocde = row.get('AREA_OCDE'),
                        ies_id = row.get('CODIGO_IES'),
                        academic_degree = row.get('GRAU')
                    )
                
                try:
                    course = CoursesModel(**course_instance.dict(exclude_unset=True))
                    session.add(course)
                    await session.commit()
                    await session.refresh(course)
                    print(f"{Fore.GREEN}Added successfully Instance {Fore.CYAN}{course.id}{Fore.GREEN} - course: {Fore.CYAN}{course.name}")
                    
                except Exception as e:
                    print(f"Erro na instancia {Fore.RED}{course_instance.id} - {course_instance.name}{Fore.WHITE}: {Fore.YELLOW}{str(e)}")
                    await session.rollback()
                    lines_with_error.append(row)
                    continue
            
            if lines_with_error:
                with open("src/Scripts/CSVs/courses_with_error.csv", "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["CODIGO_CURSO", "NOME_CURSO", "GRAU", "AREA_OCDE", "CODIGO_IES"])
                    writer.writerows(lines_with_error) 

if __name__ == "__main__":
    asyncio.run(add_cursos())