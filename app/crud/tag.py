from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    def get_with_name(
        self, db: Session, *, name: str 
    ) -> List[Tag]:
        return db.query(self.model)\
            .filter(Tag.name.like(f"%{name}%"))\
            .order_by(Tag.name).all()

tag = CRUDTag(Tag)