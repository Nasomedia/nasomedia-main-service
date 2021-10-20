from sqlalchemy import Column, Integer, String

from app.db.base import Base

class Publisher(Base):
    __tablename__ = "publisher"
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    profile_url = Column(String, nullable=True)
    