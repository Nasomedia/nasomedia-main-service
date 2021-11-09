from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Genre
from app.schemas import GenreCreate, GenreUpdate

class CRUDGenre(CRUDBase[Genre, GenreCreate, GenreUpdate]):
    def get_multi(
        self, 
        db: Session,
        *, 
        keyword: Optional[str] = None
    ) -> List[Genre]:
        if keyword:
            return db.query(self.model)\
                .filter(Genre.name.like(f"%{keyword}%"))\
                .order_by(Genre.name)\
                .all()
        return db.query(self.model)\
            .order_by(Genre.name)\
            .all() 

genre = CRUDGenre(Genre)