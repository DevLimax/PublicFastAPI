from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

#Schemas que vão servir como corpo para as colunas (instituitions) e (cities)
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

#-----------------------------------------------------------

#Schemas que vão ser utilizados pelo endpoint como Serializer
class StatesSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    uf: str

    model_config = ConfigDict(from_attributes=True)

class StatesSchemaWithRelations(StatesSchemaBase):
    cities: List[SchemaCitiesForState]
    instituitions: List[SchemaIesToState]

    model_config = dict(from_attributes=True)

#-----------------------------------------------------------

#Schemas utilizados para documentar os Responses HTTP
class StatesSchemaResponse(StatesSchemaBase):
    id: int= 5
    name: str = "São Paulo"
    uf: str = "SP"

class StatesSchemaWithRelationsResponse(StatesSchemaResponse):
    cities: List[SchemaCitiesForState] = [{"id": 29100274, "name": "Campinas"}]
    instituitions: List[SchemaIesToState] = [{"id": 5102, "name": "Universidade Estadual De Campinas", "abbreviation": "UNICAMP", "type": "Estadual", "city": {"id": 29100274, "name": "Campinas"}, "site": "www.ies.example.br"}]

#-----------------------------------------------------------

#Filtros
class StateFilters(BaseModel):
    uf: Optional[str] = Field(None, description="Sigla do estado")

