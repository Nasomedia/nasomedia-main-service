from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .publisher import Publisher
from .publisher import Publisher

class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, nullable=False)
    
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    
    thumbnail_url = Column(String, nullable=False)
    
    publisher_id = Column(Integer, ForeignKey(
        "publisher.id", ondelete="CASCADE"), nullable=True)
    publisher = relationship(Publisher)