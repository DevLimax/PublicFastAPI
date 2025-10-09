from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from publicapi.models.coursesModel import CoursesModel
from publicapi.schemas.instituitionSchema import InstituitionSchemaBase, IesSchemaResponse

#Schemas que vão servir como corpo para a coluna (city) em CourseLocations:
class CitieSchemaToCourses(BaseModel):
    id: Optional[int] = None
    name: str
    
#-----------------------------------------------------------

"""
Schemas do Model CourseLocations:

Esse Schema é apenas referencia para os dados da tabela (CourseLocations), essa tabela não tera um endpoint propio, sera utilizada junto com o endpoint (courses);
para complementar os dados de um curso, trazendo localidade (cidade - estado), modalidade, carga horária e quantidade de vagas de um curso.

cada curso tem seu codigo propio e cada curso pertence a uma universidade, mas cada curso tem localidades diferentes de disponibilidade, por isso essa tabela foi feita,
para funcionar como uma especie de tabela de relacionamento, many to many
"""
class CourseLocationSchema(BaseModel):
    course_id: Optional[int] = None
    modality: Optional[str] = None
    workload: Optional[float] = None
    quantity_vacancies: Optional[int] = None
    situation: Optional[str]
    city: Optional[CitieSchemaToCourses]
    
    model_config = ConfigDict(from_attributes=True)

#-----------------------------------------------------------

"""
Schemas para documentar os Responses HTTP:
"""

class CourseSchemaResponse(BaseModel):
    id: Optional[int] = 1
    name: str = "Engenharia de software"
    area_ocde: Optional[str] = "Formação de profissional de desenvolvimento"
    academic_degree: str = "Bacharelado"
    ies: IesSchemaResponse

class CourseSchemaWithRelationsResponse(CourseSchemaResponse):
    locations: Optional[List[CourseLocationSchema]] = [{"course_id": 1, "modality": "Presencial", "workload": 3100.0, "quantity_vacancies": 54, "situation": "em Atividade", "city": {"id": 68100221, "name": "Sorocaba"}}]

#-----------------------------------------------------------

"""
Schemas utilizados pela API como Serializers:

CoursechemaBase: Schema utilizado para serializar os dados de um curso existente no banco de dados, para um objeto JSON

CourseSchemaCreate: Schema utilizado para serializar um objeto Json enviado pelo usuário, para uma instancia no banco de dados

CourseWithRelations: Schema herda as colunas de (CourseSchemaBase) e adiciona a coluna (locations) uma relação com a tabela (CourseLocations) trazendo dados complementares
                     como localidade (ciadade - estado), modalidade, carga horária e quantidade de vagas de um curso.
"""
class CourseSchemaBase(BaseModel):

    id: Optional[int] = None
    name: str
    area_ocde: Optional[str] = None
    academic_degree: str
    ies: Optional[InstituitionSchemaBase]
    
    model_config = ConfigDict(from_attributes=True)
    
class CourseSchemaCreate(BaseModel):
    id: int
    name: str
    area_ocde: Optional[str] = None
    ies_id: int
    academic_degree: CoursesModel.DegreeChoices 
    
class CourseWithRelations(CourseSchemaBase):
    locations: Optional[List[CourseLocationSchema]] = None
    
    model_config = ConfigDict(from_attributes=True)
    
#-----------------------------------------------------------
    
"""
Schemas de filtros:

Os filtros disponiveis para o Endpoint (courses) são: 
name: String - Nome do curso, suporta (ilike) - EX: "sistemas de informação
academic_degree: String - Grau acadêmico do curso, suporta (ilike) - EX: "bacharelado
ies_id: Integer - ID (codigo) da Instituição de ensino - EX: 583 (CODIGO DA UFC)

OBS: no filtro (name) terá que tomar cuidado com as acentuações, problema ainda não tratado!
"""
class CourseFilters(BaseModel):
    name: Optional[str] = Field(None, description="Nome do curso")
    academic_degree: Optional[str] = Field(None, description="Grau acadêmico do curso")
    ies_id: Optional[int] = Field(None, description="ID (codigo) da Instituição de ensino")
    
