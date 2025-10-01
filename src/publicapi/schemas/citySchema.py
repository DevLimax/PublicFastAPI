from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from publicapi.schemas.stateSchema import StatesSchemaBase

class CitiesSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    state: StatesSchemaBase
    
    model_config = ConfigDict(from_attributes=True)
        
class CitiesSchemaCreate(BaseModel):
    id: int
    name: str
    state_id: int

class SchemaIesForCity(BaseModel):
    id: Optional[int] = None
    name: str
    abbreviation: Optional[str] = None
    type: str
    site: Optional[str] = None
    
class CitiesSchemaWithRelations(CitiesSchemaBase):
    instituitions: Optional[List[SchemaIesForCity]]
    
class CitiesFilters(BaseModel):
    uf: Optional[str] = None
    name: Optional[str] = None