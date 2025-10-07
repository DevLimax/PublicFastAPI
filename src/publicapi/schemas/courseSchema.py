from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from publicapi.models.coursesModel import CoursesModel
from publicapi.schemas.instituitionSchema import InstituitionSchemaBase
from publicapi.schemas.citySchema import CitiesSchemaBase

class CourseSchemaBase(BaseModel):

    id: Optional[int] = None
    name: str
    area_ocde: Optional[str] = None
    academic_degree: str
    ies: InstituitionSchemaBase
    
    model_config = ConfigDict(from_attributes=True)
    
class CourseSchemaCreate(BaseModel):
    id: int
    name: str
    area_ocde: Optional[str] = None
    ies_id: int
    academic_degree: CoursesModel.DegreeChoices 
    
class CourseFilters(BaseModel):
    name: Optional[str] = None
    academic_degree: Optional[CoursesModel.DegreeChoices] = None
    ies_id: Optional[int] = None
    
# Esquemas do Model CourseLocations
class CourseLocationSchemaBase(BaseModel):
    id: Optional[int] = None
    course: CourseSchemaBase
    modality: Optional[str] = None
    workload: Optional[float] = None
    quantity_vacancies: Optional[int] = None
    situation: Optional[str]
    city: CitiesSchemaBase
    
    model_config = ConfigDict(from_attributes=True)
    
class CourseLocationsSchemaCreate(BaseModel):
    course_id: int
    city_id: int
    workload: Optional[float] = None
    modality: Optional[str] = None
    situation: Optional[str] = None
    quantity_vacancies: Optional[int] = None
    
