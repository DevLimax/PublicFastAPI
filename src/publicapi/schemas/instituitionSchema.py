from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from publicapi.models.iesModel import IesModel

class InstituitionSchemaBase(BaseModel):

    id: Optional[int] = None
    name: str
    abbreviation: str
    type: IesModel.TypeChoices
    state_uf: str
    city_name: str
    quantity_campus: int
    site: str

    model_config = ConfigDict(from_attributes=True)


class InstituitionSchemaCreate(BaseModel):

    id: int
    name: str
    abbreviation: str
    type: IesModel.TypeChoices
    state_id: int
    city_id: int
    site: Optional[str]
    is_active: Optional[bool] = None
    
