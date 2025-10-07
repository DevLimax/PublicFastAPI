from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum as EnumSQL
from publicapi.models import BaseModel
from enum import Enum

class CoursesModel(BaseModel):
    __tablename__ = "cursos"

    class DegreeChoices(str, Enum):
        BACHARELADO = "Bacharelado"
        LICENCIATURA = "Licenciatura"
        TECNOLOGO = "Tecnologo"
        MESTRADO = "Mestrado"
        DOUTORADO = "Doutorado"
        ESPECIALIZACAO = "Especialização"
        AREA_DE_INGRESSO_BASICO = "ABI"
        SEQUENCIAL = "Sequencial"
        NAO_IDENTIFICADO = "Não identificado"
        
    class SituationChoices(str, Enum):
        EM_ATIVIDADE = "Em atividade"
        EXTINTO = "Extinto"
        EM_EXTINCAO = "Em extinção"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    ies_id: Mapped[int] = mapped_column(ForeignKey("instituicoes.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    area_ocde: Mapped[str] = mapped_column(nullable=True)
    academic_degree: Mapped[DegreeChoices] = mapped_column(EnumSQL(DegreeChoices), default=DegreeChoices.NAO_IDENTIFICADO, nullable=False)
    
    ies = relationship("IesModel", back_populates="courses")
    locations = relationship("CourseLocationsModel", back_populates="course")
    
    def validate_data(self):
        if self.name and self.name != "":
            self.name = self.name.title()
        else:
            raise ValueError("A coluna (Name) não pode ser vazia")
        
        if self.area_ocde and self.area_ocde != "":
            self.area_ocde = self.area_ocde.title()
        else:
            self.area_ocde = None

        
