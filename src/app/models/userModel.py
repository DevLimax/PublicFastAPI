from sqlalchemy.orm import Mapped, mapped_column
from .baseModel import BaseModel

class UserModel(BaseModel):
    __tablename__ = "usuarios"
    
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    