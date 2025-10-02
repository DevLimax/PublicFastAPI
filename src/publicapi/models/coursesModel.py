from sqlalchemy.orm import Mapped, mapped_column
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

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    area_ocde: Mapped[str] = mapped_column(nullable=True)
    academic_degree: Mapped[DegreeChoices] = mapped_column(EnumSQL(DegreeChoices), default=DegreeChoices.NAO_IDENTIFICADO, nullable=False)
    workload: Mapped[float] = mapped_column(nullable=False)
    
    def validate_data(self):
        if self.name and self.name != "":
            self.name = self.name.title()
        else:
            raise ValueError("A coluna (Name) não pode ser vazia")

        if self.area_ocde and self.area_ocde != "":
            self.area_ocde = self.area_ocde.title()
        else:
            self.area_ocde = None

        if not self.workload:
            raise ValueError("A coluna (Workload) não pode ser vazia")
        
