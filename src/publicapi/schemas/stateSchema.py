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
class StatesSchemaWithRelations(StatesSchemaBase):
    cities: List[SchemaCitiesForState]

class StateFilters(BaseModel):
    uf: Optional[str] = None    

