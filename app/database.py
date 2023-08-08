from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import settings


database_url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@/{settings.db_name}?host={settings.db_host}"
engine = create_async_engine(settings.database_url)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
