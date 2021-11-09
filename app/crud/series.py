from typing import Any, Optional, List, Dict, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text

from app.crud.base import CRUDBase
from app.models.series import Series
from app.schemas.series import SeriesCreate, SeriesUpdate
from app.schemas.sort_enum import  SeriesSortEnum

from .utils import get_kst_now, sync_update_date

import sqlalchemy

class CRUDSeries(CRUDBase[Series, SeriesCreate, SeriesUpdate]):
    def get_multi(
        self, 
        db: Session,
        *,
        sort_by: SeriesSortEnum = "id",
        keyword: Optional[str] = None,
        desc: bool = True,
        **kwargs
    ) -> List[Series]:
        direction = sqlalchemy.desc if desc else sqlalchemy.asc
        if keyword:
            return db.query(self.model)\
                .filter(Series.title.like(f"%{keyword}%"))\
                .filter_by(**kwargs)\
                .order_by(direction(getattr(Series, sort_by))).all()
    
        return db.query(self.model)\
            .filter_by(**kwargs)\
            .order_by(direction(getattr(Series, sort_by))).all()
    
    def create(self, db: Session, *, obj_in: SeriesCreate) -> Series:
        obj_in_data = jsonable_encoder(obj_in)

        db_obj = self.model(**obj_in_data)
        db_obj.created_at = get_kst_now()
        db.add(db_obj)
        db.commit()
        sync_update_date(db=db, now=db_obj.created_at, series_id=db_obj.id)
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: Series,
        obj_in: Union[SeriesUpdate, Dict[str, Any]]
    ) -> Series:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db_obj.updated_at = get_kst_now()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

series = CRUDSeries(Series)