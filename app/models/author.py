from sqlalchemy import Column, Integer, String, Text

from app.db.base import Base

class Author(Base):
    __tablename__ = "publisher"
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    profile_url = Column(String, nullable=True)
    