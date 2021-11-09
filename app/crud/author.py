from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Author
from app.schemas import AuthorCreate, AuthorUpdate

class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    def get_multi(
        self, 
        db: Session, 
        *, 
        keyword: Optional[str] = None 
    ) -> List[Author]:
        if keyword:
            return db.query(self.model)\
                    .filter(Author.name.like(f"%{keyword}%"))\
                    .order_by(Author.name)\
                    .all()
        return db.query(self.model)\
            .order_by(Author.name)\
            .all()

author = CRUDAuthor(Author)