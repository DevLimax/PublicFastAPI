from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from publicapi.models import BaseModel

class CampiModel(BaseModel):
    __tablename__= "campi"
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    ies_id: Mapped[int] = mapped_column(ForeignKey("instituicoes.id"), nullable=False)
    state_id: Mapped[int] = mapped_column(ForeignKey("estados.id"), nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("municipios.id"), nullable=False)
    cep: Mapped[str] = mapped_column(nullable=True)
    district: Mapped[str] = mapped_column(nullable=True)
    street: Mapped[str] = mapped_column(nullable=True)
    number: Mapped[str] = mapped_column(nullable=True, default="S/N")
    telephone: Mapped[str] = mapped_column(nullable=True, unique=True)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    
    ies = relationship("IesModel", back_populates="campi")
    state = relationship("StatesModel", back_populates="campi")
    city = relationship("CitiesModel", back_populates="campi")
    
    def validate_data(self):
        
        for attr in ("cep", "district", "street", "number", "telephone", "email"):
            
            if self.name:
                self.name = self.name.title()
            else:
                raise ValueError("O campo 'name' é obrigatório.")
            
            if getattr(self, attr) == "":
                setattr(self, attr, None)
            
            if self.district:
                self.district = self.district.title()
            
            if self.street:
                self.street = self.street.title()
            
        return self
    
    
    
    