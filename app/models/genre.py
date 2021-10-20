from sqlalchemy import Column, Integer, String

from app.db import Base

class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
