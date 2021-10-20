from app.crud.base import CRUDBase
from app.models.series_author import SeriesAuthor
from app.schemas.series_author import SeriesAuthorCreate, SeriesAuthorUpdate


class CRUDSerieAuthor(CRUDBase[SeriesAuthor, SeriesAuthorCreate, SeriesAuthorUpdate]):
    pass

series_author = CRUDSerieAuthor(SeriesAuthor)