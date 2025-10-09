from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from publicapi.models.iesModel import IesModel
from publicapi.schemas.stateSchema import StatesSchemaBase, StatesSchemaResponse

#Schemas que vão servir como corpo para as colunas (city, courses)
class SchemaCityToIes(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)
    
class SchemaCoursesToIes(BaseModel):
    id: int
    name: str
    area_ocde: Optional[str] = None
    academic_degree: str
   
    model_config = ConfigDict(from_attributes=True)
    
#-----------------------------------------------------------
    
#Schema de cursos, com localização e dados como modalidade, carga horária e quantidade de vagas
class SchemaCourseLocations(BaseModel):
    modality: Optional[str] = None
    workload: Optional[float] = None
    quantity_vacancies: Optional[int] = None
    situation: Optional[str]
    city: Optional[SchemaCityToIes]
    
    model_config = ConfigDict(from_attributes=True)

#-----------------------------------------------------------

#Schemas utilizados pela API como Serializers
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

#-----------------------------------------------------------

#Schemas para documentar os Responses HTTP
class IesSchemaResponse(BaseModel):
    id: Optional[int] = 5102
    name: str = "Centro Universitário de Campinas"
    abbreviation: Optional[str] = "UNICAMP"
    type: IesModel.TypeChoices = IesModel.TypeChoices.ESTADUAL
    state: StatesSchemaResponse
    city: Optional[SchemaCityToIes] = SchemaCityToIes(id=29100274, name="Campinas")
    site: Optional[str] = "www.ies.example.br"
    
class IesSchemaWithRelationsReponse(IesSchemaResponse):
    courses: Optional[List[SchemaCoursesToIes]] = [{"id": 1, "name": "Matemática", "area_ocde": "Formação de professor de matemática", "academic_degree": "Licenciatura"}]
    
#Schema de filtros
class IesFilters(BaseModel):
    abbreviation: Optional[str] = None
    type: Optional[str] = None
    uf: Optional[str] = None
    city_name: Optional[str] = None
    city_code: Optional[int] = None
    
    
