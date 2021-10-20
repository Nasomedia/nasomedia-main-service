from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .series import Series
    from .author import Author

class SeriesAuthor(Base):
    __tablename__ = "series_author"
    id = Column(Integer, primary_key=True, index=True)

    series_id = Column(Integer, ForeignKey(
        "series.id", ondelete="CASCADE"), nullable=False)

    author_id = Column(Integer, ForeignKey(
        "author.id", ondelete="CASCADE"), nullable=False)

    series = relationship(Series)
    author = relationship(Author)