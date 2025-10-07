from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from publicapi.models.coursesModel import CoursesModel
from publicapi.schemas.instituitionSchema import InstituitionSchemaBase

class CourseSchemaBase(BaseModel):

    id: Optional[int] = None
    name: str
    area_ocde: Optional[str] = None
    academic_degree: str
    ies: Optional[InstituitionSchemaBase]
    
    model_config = ConfigDict(from_attributes=True)
    
class CourseSchemaCreate(BaseModel):
    id: int
    name: str
    area_ocde: Optional[str] = None
    ies_id: int
    academic_degree: CoursesModel.DegreeChoices 
    
class CourseFilters(BaseModel):
    name: Optional[str] = Field(None, description="Nome do curso")
    academic_degree: Optional[CoursesModel.DegreeChoices] = Field(None, description="Grau acadêmico do curso (Ex: Bacharelado, Licenciatura).")
    ies_id: Optional[int] = Field(None, description="ID (codigo) da Instituição de ensino")
    
class CitieSchemaToCourses(BaseModel):
    id: Optional[int] = None
    name: str
    
# Esquemas do Model CourseLocations
class CourseLocationSchema(BaseModel):
    course_id: Optional[int] = None
    modality: Optional[str] = None
    workload: Optional[float] = None
    quantity_vacancies: Optional[int] = None
    situation: Optional[str]
    city: Optional[CitieSchemaToCourses]
    
    model_config = ConfigDict(from_attributes=True)
    
class CourseWithRelations(CourseSchemaBase):
    locations: Optional[List[CourseLocationSchema]] = None
    
    model_config = ConfigDict(from_attributes=True)
    

    
