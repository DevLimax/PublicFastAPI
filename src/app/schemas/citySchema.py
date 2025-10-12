from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from app.schemas.stateSchema import StatesSchemaBase, StatesSchemaResponse

#Schemas que vão servir como corpo para as colunas (instituitions)
class SchemaIesForCity(BaseModel):
    id: Optional[int] = None
    name: str
    abbreviation: Optional[str] = None
    type: str
    site: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

#-----------------------------------------------------------

#Schemas utilizados pela API como Serializers
class CitiesSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    state: StatesSchemaBase
    
    model_config = ConfigDict(from_attributes=True)
        
class CitiesSchemaCreate(BaseModel):
    id: int
    name: str
    state_id: int
    
class CitiesSchemaWithRelations(CitiesSchemaBase):
    instituitions: Optional[List[SchemaIesForCity]]
    
    model_config = ConfigDict(from_attributes=True)
    
#-----------------------------------------------------------

#Schemas para documentar os Responses HTTP
class CitiesSchemaResponse(BaseModel):
    id: Optional[int] = "29100274"
    name: str = "Campinas"
    state: StatesSchemaResponse
    
class CitiesSchemaWithRelationsResponse(CitiesSchemaResponse):
    instituitions: Optional[List[SchemaIesForCity]] = [{"id": 5102, "name": "Universidade Estadual De Campinas", "abbreviation": "UNICAMP", "type": "Estadual", "site": "www.ies.example.br"}]

#-----------------------------------------------------------    
    
#Schema de filtros
class CitiesFilters(BaseModel):
    uf: Optional[str] = None
    name: Optional[str] = None
    
