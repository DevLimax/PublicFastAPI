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

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    academic_degree: Mapped[DegreeChoices] = mapped_column(EnumSQL(DegreeChoices), default=DegreeChoices.NAO_IDENTIFICADO, nullable=False)
    workload: Mapped[float] = mapped_column(nullable=False)

    

