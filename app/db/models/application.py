from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    active = Column(Boolean, default=True)
    blob_connection_string = Column(String, nullable=False)
    blob_container = Column(String, nullable=False)
