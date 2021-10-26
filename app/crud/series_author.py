from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import SeriesAuthor, Series, Author
from app.schemas import SeriesAuthorCreate, SeriesAuthorUpdate


class CRUDSerieAuthor(CRUDBase[SeriesAuthor, SeriesAuthorCreate, SeriesAuthorUpdate]):
    def get_serieses_with_author(
        self,
        db: Session,
        *,
        author_id: int
    ) -> List[Series]:
        return db.query(Series)\
            .join(SeriesAuthor, Series.id == SeriesAuthor.series_id)\
            .filter(SeriesAuthor.author_id == author_id)\
            .all()

    def get_authors_with_series(
        self,
        db: Session,
        *,
        series_id: int
    ) -> List[Author]:
        return db.query(Author)\
            .join(SeriesAuthor, Author.id == SeriesAuthor.author_id)\
            .filter(SeriesAuthor.series_id == series_id)\
            .all()


series_author = CRUDSerieAuthor(SeriesAuthor)