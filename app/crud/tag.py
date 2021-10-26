from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Tag
from app.schemas import TagCreate, TagUpdate

class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    def get_multi(
        self, 
        db: Session,
        *, 
        keyword: Optional[str] = ""
    ) -> List[Tag]:
        return db.query(self.model)\
            .filter(Tag.name.like(f"%{keyword}%"))\
            .order_by(Tag.name)\
            .all()

tag = CRUDTag(Tag)