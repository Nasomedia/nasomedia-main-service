from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .series import Series
from .series import Series

class Episode(Base):
    __tablename__ = "episode"
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    order = Column(Integer, nullable=False, index=True)
    
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    
    thumbnail_url = Column(String, nullable=False)
    
    is_book = Column(Boolean, nullable=False)
    book_id = Column(Integer, nullable=True)

    series_id = Column(Integer, ForeignKey(
        "series.id", ondelete="CASCADE"), nullable=False)
    series = relationship(Series)