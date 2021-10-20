from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .series import Series
    from .tag import Tag

from .series import Series
from .tag import Tag

class SeriesTag(Base):
    __tablename__ = "series_tag"
    id = Column(Integer, primary_key=True, index=True)

    series_id = Column(Integer, ForeignKey(
        "series.id", ondelete="CASCADE"), nullable=False)

    tag_id = Column(Integer, ForeignKey(
        "tag.id", ondelete="CASCADE"), nullable=False)

    series = relationship(Series)
    tag = relationship(Tag)