from typing import Generic, TypeVar, Type, Any, Optional, List, Dict, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text

from app.crud.base import CRUDBase
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate

from .utils import get_kst_now, sync_update_date

class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    def get_with_name(
        self, db: Session, *, name: str 
    ) -> List[Author]:
        return db.query(self.model)\
            .filter(Author.name.like(f"%{name}%"))\
            .order_by(self.model.order).all()
    

author = CRUDAuthor(Author)