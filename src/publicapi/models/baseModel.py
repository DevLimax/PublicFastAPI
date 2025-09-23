from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from publicapi.core.configs import settings
from datetime import datetime

class BaseModel(settings.DBBASEMODEL):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, 
                                                 default=datetime.now(), 
                                                 server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=True, default=datetime.now, onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    