from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import SeriesTag, Series, Tag
from app.schemas import SeriesTagCreate, SeriesTagUpdate


class CRUDSerieTag(CRUDBase[SeriesTag, SeriesTagCreate, SeriesTagUpdate]):
    def get_serieses_with_tag(
        self,
        db: Session,
        *,
        tag_id: int
    ) -> List[Series]:
        return db.query(Series)\
            .join(SeriesTag, Series.id == SeriesTag.series_id)\
            .filter(SeriesTag.tag_id == tag_id)\
            .all()

    def get_tags_with_series(
        self,
        db: Session,
        *,
        series_id: int
    ) -> List[Tag]:
        return db.query(Tag)\
            .join(SeriesTag, Tag.id == SeriesTag.tag_id)\
            .filter(SeriesTag.series_id == series_id)\
            .all()

        
    def delete_tags_with_series(
        self,
        db: Session,
        *,
        series_id: int,
    ) -> List[Tag]:
        obj = db.query(self.model).filter(self.model.series_id == series_id).all()
        db.delete(obj)
        db.commit()
        return obj

series_tag = CRUDSerieTag(SeriesTag)