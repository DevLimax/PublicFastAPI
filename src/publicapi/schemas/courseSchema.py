from pydantic import BaseModel
from typing import Optional, List
from publicapi.models.coursesModel import CoursesModel

class CourseSchemaBase(BaseModel):

    id: Optional[int] = None
    name: str
    area_ocde: Optional[str] = None
    workload: float
    academic_degree: str

class CourseFilters(BaseModel):
    name: Optional[str] = None
    workload: Optional[float] = None
    academic_degree: Optional[CoursesModel.DegreeChoices] = None
