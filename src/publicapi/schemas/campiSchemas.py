from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from publicapi.schemas.stateSchema import StatesSchemaBase

class SchemaIesToCampi(BaseModel):
    id: int
    name: str
    abbreviation: Optional[str] = None
    type: str
    site: str
    
    model_config = ConfigDict(from_attributes=True)
    
class SchemaCityToCampi(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
    
class CampiSchemaBase(BaseModel):
    id: int
    name: str
    ies: SchemaIesToCampi
    state:  StatesSchemaBase
    city: SchemaCityToCampi
    cep: Optional[str] = None
    district: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class CampiSchemaCreate(BaseModel):
    id: int
    name: str
    ies_id: int
    state_id: int
    city_id: int
    cep: Optional[str] = None
    district: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    

    