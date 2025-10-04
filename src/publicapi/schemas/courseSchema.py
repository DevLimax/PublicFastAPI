from pydantic import BaseModel
from typing import Optional, List
from publicapi.models.coursesModel import CoursesModel
from publicapi.schemas.instituitionSchema import InstituitionSchemaBase

class CourseSchemaBase(BaseModel):

    id: Optional[int] = None
    name: str
    area_ocde: Optional[str] = None
    academic_degree: str
    ies: InstituitionSchemaBase
    
class CourseSchemaCreate(BaseModel):
    id: int
    name: str
    area_ocde: Optional[str] = None
    ies_id: int
    academic_degree: CoursesModel.DegreeChoices 
    
class CourseFilters(BaseModel):
    name: Optional[str] = None
    academic_degree: Optional[CoursesModel.DegreeChoices] = None
