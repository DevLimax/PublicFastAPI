from sqlalchemy.orm import Mapped, mapped_column
from .baseModel import BaseModel

class UserModel(BaseModel):
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    