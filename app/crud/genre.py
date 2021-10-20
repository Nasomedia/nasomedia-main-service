from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate

class CRUDGenre(CRUDBase[Genre, GenreCreate, GenreUpdate]):
    def get_with_name(
        self, db: Session, *, name: str 
    ) -> List[Genre]:
        return db.query(self.model)\
            .filter(Genre.name.like(f"%{name}%"))\
            .order_by(Genre.name).all()

genre = CRUDGenre(Genre)