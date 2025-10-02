from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class StatesSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    uf: str

    model_config = ConfigDict(from_attributes=True)
class SchemaCitiesForState(BaseModel):
    id: Optional[int] = None
    name: str        
    
    model_config = ConfigDict(from_attributes=True)

class SchemaIesToState(BaseModel):
    id: Optional[int]
    name: str
    abbreviation: Optional[str] = None
    type: str
    city: SchemaCitiesForState
    site: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class StatesSchemaWithRelations(StatesSchemaBase):
    cities: List[SchemaCitiesForState]
    instituitions: List[SchemaIesToState]

    model_config = dict(from_attributes=True)

class StateFilters(BaseModel):
    uf: Optional[str] = None  
    city_name: Optional[str] = None    
    city_code: Optional[int] = None

