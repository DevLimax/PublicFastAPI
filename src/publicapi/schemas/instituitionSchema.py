from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from publicapi.models.iesModel import IesMOdel

class InstituitionSchemaBase(BaseModel):

    id: Optional[int] = None
    name: str
    abbreviation: str
    type: IesMOdel.TypeChoices
    quantity_campus: int
    state_uf: str
    site: str

    model_config = ConfigDict(from_attributes=True)


class InstituitionSchemaCreate(BaseModel):

    id: Optional[int] = None
    name: str
    abbreviation: str
    type: IesMOdel.TypeChoices
    quantity_campus: int
    state_id: int
    site: str