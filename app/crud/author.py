from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate

class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    def get_with_name(
        self, db: Session, *, name: str 
    ) -> List[Author]:
        return db.query(self.model)\
            .filter(Author.name.like(f"%{name}%"))\
            .order_by(self.model.order).all()
    

author = CRUDAuthor(Author)