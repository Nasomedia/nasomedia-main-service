from app.crud.base import CRUDBase
from app.models.series_tag import SeriesTag
from app.schemas.series_tag import SeriesTagCreate, SeriesTagUpdate


class CRUDSerieTag(CRUDBase[SeriesTag, SeriesTagCreate, SeriesTagUpdate]):
    pass

series_tag = CRUDSerieTag(SeriesTag)