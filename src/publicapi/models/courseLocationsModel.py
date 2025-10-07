from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from publicapi.models import BaseModel

class CourseLocationsModel(BaseModel):
    __tablename__ = "cursos_localização"
    
    course_id: Mapped[int] = mapped_column(ForeignKey("cursos.id"), nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("municipios.id"), nullable=False)
    workload: Mapped[float] = mapped_column(nullable=True)
    modality: Mapped[str] = mapped_column(nullable=False)
    situation: Mapped[str] = mapped_column(nullable=False)
    quantity_vacancies: Mapped[int] = mapped_column(nullable=True)
    
    course = relationship("CoursesModel", back_populates="locations")
    city = relationship("CitiesModel", back_populates="courses")