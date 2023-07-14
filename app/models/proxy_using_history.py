from sqlalchemy import Column, Integer, DateTime, sql, String

from . import Base


class ProxyUsingHistory(Base):
    __tablename__ = "proxy_using_history"

    id = Column(Integer, primary_key=True, index=True)
    proxy_id = Column(Integer, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=sql.func.current_timestamp(), nullable=False)
    job_name = Column(String(255), nullable=False)
