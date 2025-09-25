from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum as EnumSQL, URL
from publicapi.models import BaseModel
from enum import Enum

class IesMOdel(BaseModel):
    __tablename__ = "instituicoes"

    class TypeChoices(str, Enum):
        FEDERAL = "Federal"
        ESTADUAL = "Estadual"
        MUNICIPAL = "Municipal"
        OUTRO = "Outro"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    abbreviation: Mapped[str] = mapped_column(nullable=False, unique=True)
    type: Mapped[TypeChoices] = mapped_column(EnumSQL(TypeChoices), default=TypeChoices.OUTRO, nullable=False)
    quantity_campus: Mapped[int] = mapped_column(nullable=False, default=0)
    state_id: Mapped[int] = mapped_column(nullable=False)
    site: Mapped[str] = mapped_column(nullable=False)

    state = relationship("StateModel", back_populates="ies", lazy="joined")
    
    @property
    def state_uf(self):
        return self.state.id
    
