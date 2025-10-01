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

class SchemaIesForState(BaseModel):
    id: Optional[int]
    name: str
    abbreviation: str
    type: str
    city_name: str
    quantity_campus: int
    site: str

    model_config = ConfigDict(from_attributes=True)


class StatesSchemaWithRelations(StatesSchemaBase):
    cities: List[SchemaCitiesForState]
    instituitions: List[SchemaIesForState]

    model_config = dict(from_attributes=True)

class StateFilters(BaseModel):
    uf: Optional[str] = None  
    city_name: Optional[str] = None    
    city_code: Optional[int] = None

