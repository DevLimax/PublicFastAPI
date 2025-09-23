from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,  AsyncEngine
from publicapi.core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = sessionmaker(
    autoflush=True,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)