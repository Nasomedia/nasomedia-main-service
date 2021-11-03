from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .series import Series
    from .genre import Genre
from .series import Series
from .genre import Genre

class SeriesGenre(Base):
    __tablename__ = "series_genre"
    id = Column(Integer, primary_key=True, index=True)

    series_id = Column(Integer, ForeignKey(
        "series.id", ondelete="CASCADE"), nullable=False)

    genre_id = Column(Integer, ForeignKey(
        "genre.id", ondelete="CASCADE"), nullable=False)

    series = relationship(Series)
    genre = relationship(Genre)