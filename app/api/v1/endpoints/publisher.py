from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query, Path
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.api.v1 import deps

router = APIRouter()

@router.get("", response_model=List[schemas.Genre])
def read_publishers(
    db: Session = Depends(deps.get_db),
    *,
    keyword: Optional[str] = Query(
        "",
        title="검색 키워드"
    )
):
    """
    Retrieve publisher
    """
    publishers = crud.publisher.get_multi(
        db, keyword=keyword
    )
    return publishers

@router.post("", response_model=schemas.Publisher)
def create_publisher(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    publisher_in: schemas.PublisherCreate
):
    """
    Create new publisher
    """
    publisher = crud.publisher.create(db, obj_in=publisher_in)
    return publisher

@router.put("/{publisher_id}")
def update_publisher(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    publisher_id: int = Path(..., ge=1),
    publisher_in: schemas.PublisherUpdate
):
    """
    Update publisher
    """
    publisher = crud.publisher.get(db, id=publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher

@router.delete("/{publihser_id}")
def delete_publisher(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    publisher_id: int = Path(..., ge=1)
):
    publisher = crud.publisher.get(db, id=publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
