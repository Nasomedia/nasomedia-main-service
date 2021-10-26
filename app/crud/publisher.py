from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.publisher import Publisher
from app.schemas.publisher import PublisherCreate, PublisherUpdate

class CRUDPublisher(CRUDBase[Publisher, PublisherCreate, PublisherUpdate]):
    def get_multi(
        self, 
        db: Session, 
        *, 
        keyword: Optional[str] = "" 
    ) -> List[Publisher]:
        return db.query(self.model)\
            .filter(Publisher.name.like(f"%{keyword}%")).all()

publisher = CRUDPublisher(Publisher)