from app.crud.base import CRUDBase
from app.models.series_genre import SeriesGenre
from app.schemas.series_genre import SeriesGenreCreate, SeriesGenreUpdate


class CRUDSerieGenre(CRUDBase[SeriesGenre, SeriesGenreCreate, SeriesGenreUpdate]):
    pass

series_genre = CRUDSerieGenre(SeriesGenre)