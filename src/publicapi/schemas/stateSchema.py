from pydantic import BaseModel
from typing import Optional, List

class StatesSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    uf: str

    class Config:
        from_attributes = True

