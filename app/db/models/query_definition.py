from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base

class QueryDefinition(Base):
    __tablename__ = "query_definitions"

    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("applications.id"))
    name = Column(String, nullable=False)
    sql_template = Column(String, nullable=False)
    db_url = Column(String, nullable=False)
    active = Column(Boolean, default=True)
