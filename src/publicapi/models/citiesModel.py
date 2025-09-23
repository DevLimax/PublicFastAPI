from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from publicapi.models import BaseModel

class CitiesModel(BaseModel):
    __tablename__ = "municipios"
    __table_args__ = (
        UniqueConstraint('name', 'state_id', name='uq_cidade_state'),
    )

    name: Mapped[str] = mapped_column(nullable=False)
    state_id: Mapped[int] = mapped_column(ForeignKey("estados.id"), nullable=False)
    
    state = relationship("StatesModel", back_populates="cities", lazy="joined")