from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from publicapi.models import BaseModel

class StatesModel(BaseModel):
    __tablename__ = "estados"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    uf: Mapped[str] = mapped_column(nullable=False, unique=True)

    cities = relationship("CitiesModel", back_populates="state", lazy="joined")
    instituitions = relationship("IesModel", back_populates="state", lazy="joined")

