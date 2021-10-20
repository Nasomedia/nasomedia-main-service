from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.series_genre import Tag
from app.schemas.series_genre import TagCreate, TagUpdate


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    pass

series_genre = CRUDTag(Tag)