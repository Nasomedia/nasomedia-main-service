from typing import Any, List, Dict, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Episode
from app.schemas import EpisodeCreate, EpisodeUpdate

from .utils import get_kst_now, sync_update_date

class CRUDEpisode(CRUDBase[Episode, EpisodeCreate, EpisodeUpdate]):
    def get_all_by_series_id(
        self, db: Session, *, series_id: int, 
    ) -> List[Episode]:
        return db.query(self.model)\
            .filter(self.model.series_id == series_id)\
            .order_by(self.model.order)\
                .all()
    
    def create(
        self, 
        db: Session, 
        *, 
        db_obj: Episode,
        obj_in: EpisodeCreate,
    ) -> Episode:
        obj_in_data = jsonable_encoder(obj_in)
        now = get_kst_now()
        db_obj = self.model(
            **obj_in_data, created_at=now, updated_at=now,
        )
        db.add(db_obj)
        db.commit()
        sync_update_date(db=db, now=db_obj.created_at, series_id=db_obj.id)
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: Episode,
        obj_in: Union[EpisodeUpdate, Dict[str, Any]]
    ) -> Episode:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        sync_update_date(db=db, now=get_kst_now(), episode_id=db_obj.id)
        db.refresh(db_obj)
        return db_obj

episode = CRUDEpisode(Episode)