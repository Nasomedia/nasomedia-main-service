from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Publisher
from app.schemas import PublisherCreate, PublisherUpdate

class CRUDPublisher(CRUDBase[Publisher, PublisherCreate, PublisherUpdate]):
    def get_multi(
        self, 
        db: Session, 
        *, 
        keyword: Optional[str] = None
    ) -> List[Publisher]:
        if keyword:
            return db.query(self.model)\
                .filter(Publisher.name.like(f"%{keyword}%"))\
                .order_by(Publisher.name)\
                .all()
        return db.query(self.model)\
            .order_by(Publisher.name)\
            .all()

publisher = CRUDPublisher(Publisher)