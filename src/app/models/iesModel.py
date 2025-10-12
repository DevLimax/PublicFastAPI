from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum as EnumSQL, URL
from app.models import BaseModel
from enum import Enum

class IesModel(BaseModel):
    __tablename__ = "instituicoes"

    class TypeChoices(str, Enum):
        FEDERAL = "Federal"
        ESTADUAL = "Estadual"
        MUNICIPAL = "Municipal"
        OUTRO = "Outro"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    abbreviation: Mapped[str] = mapped_column(nullable=True, unique=True)
    type: Mapped[TypeChoices] = mapped_column(EnumSQL(TypeChoices), default=TypeChoices.OUTRO, nullable=False)
    state_id: Mapped[int] = mapped_column(ForeignKey("estados.id"), nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("municipios.id"), nullable=True)
    site: Mapped[str] = mapped_column(nullable=True, default=None)

    state = relationship("StatesModel", back_populates="instituitions")
    city = relationship("CitiesModel", back_populates="instituitions")
    courses = relationship("CoursesModel", back_populates="ies")
    
    def validate_data(self):
        self.name = self.name.title()
        if self.abbreviation:
            self.abbreviation = self.abbreviation.upper()
        
        if self.site == "":
            self.site = None
               
        if self.type == None:
            self.type = IesModel.TypeChoices.OUTRO
    
