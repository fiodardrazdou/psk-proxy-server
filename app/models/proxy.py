from sqlalchemy import Column, Integer, DateTime, sql, String, JSON, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from . import Base


class Proxy(Base):
    __tablename__ = "proxy"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    proxy_type = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=sql.func.current_timestamp(), nullable=False)
    service_name = Column(String(255), nullable=False)
    job_names = Column(JSONB, nullable=False)
    active = Column(Boolean, nullable=False)
