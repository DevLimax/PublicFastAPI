from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from publicapi.models.iesModel import IesModel
from publicapi.schemas.stateSchema import StatesSchemaBase

class SchemaCityToIes(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)
    
class SchemaCourseLocations(BaseModel):
    modality: Optional[str] = None
    workload: Optional[float] = None
    quantity_vacancies: Optional[int] = None
    situation: Optional[str]
    city: Optional[SchemaCityToIes]
    
    model_config = ConfigDict(from_attributes=True)
    
class SchemaCoursesToIes(BaseModel):
    id: int
    name: str
    area_ocde: Optional[str] = None
    academic_degree: str
   
    model_config = ConfigDict(from_attributes=True)
class InstituitionSchemaBase(BaseModel):

    id: Optional[int] = None
    name: str
    abbreviation: Optional[str] = None
    type: IesModel.TypeChoices
    state: StatesSchemaBase 
    city: Optional[SchemaCityToIes]
    site: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
class InstituitionSchemaWithRelations(InstituitionSchemaBase):
    courses: List[SchemaCoursesToIes]

    model_config = ConfigDict(from_attributes=True)

class InstituitionSchemaCreate(BaseModel):

    id: int
    name: str
    abbreviation: Optional[str] = None
    type: IesModel.TypeChoices
    state_id: int
    city_id: Optional[int] = None
    site: Optional[str] = None
    is_active: Optional[bool] = None
    
class IesFilters(BaseModel):
    abbreviation: Optional[str] = None
    type: Optional[IesModel.TypeChoices] = None
    uf: Optional[str] = None
    city_name: Optional[str] = None
    city_code: Optional[int] = None
    
    
