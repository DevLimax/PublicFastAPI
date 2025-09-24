from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class CitiesSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    state_uf: str 
    
    model_config = ConfigDict(from_attributes=True)
        
class CitiesSchemaCreate(BaseModel):
    id: int
    name: str
    state_id: int

class CitiesSchemaWithRelations(CitiesSchemaBase):
    ... 