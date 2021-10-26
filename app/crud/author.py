from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate

class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    def get_multi(
        self, 
        db: Session, 
        *, 
        keyword: Optional[str] = "" 
    ) -> List[Author]:
        return db.query(self.model)\
            .filter(Author.name.like(f"%{keyword}%")).all()

author = CRUDAuthor(Author)