from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import SeriesGenre, Series, Genre
from app.schemas import SeriesGenreCreate, SeriesGenreUpdate


class CRUDSerieGenre(CRUDBase[SeriesGenre, SeriesGenreCreate, SeriesGenreUpdate]):
    def get_serieses_with_genre(
        self,
        db: Session,
        *,
        genre_id: int
    ) -> List[Series]:
        return db.query(Series)\
            .join(SeriesGenre, Series.id == SeriesGenre.series_id)\
            .filter(SeriesGenre.genre_id == genre_id)\
            .all()

    def get_authors_with_series(
        self,
        db: Session,
        *,
        series_id: int
    ) -> List[Genre]:
        return db.query(Genre)\
            .join(SeriesGenre, Genre.id == SeriesGenre.genre_id)\
            .filter(SeriesGenre.series_id == series_id)\
            .all()

series_genre = CRUDSerieGenre(SeriesGenre)