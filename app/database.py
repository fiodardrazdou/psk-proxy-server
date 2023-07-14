from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import settings

engine = create_async_engine(settings.database_url)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def get_db() -> AsyncSession:
    with async_session() as session:
        try:
            yield session
        finally:
            session.close()
