from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session


from app import crud, schemas, models
from app.api.v1 import deps

router = APIRouter()


@router.get("", response_model=List[schemas.Tag])
def read_tag(
    db: Session = Depends(deps.get_db),
    *,
    keyword: Optional[str] = Query(
        "",
        title="검색 키워드"
    ),
):
    """
    Retrieve tag
    """
    tags = crud.tag.get_multi(
        db, keyword=keyword
    )
    return tags


@router.post("", response_model=schemas.Tag)
def create_tag(
    db: Session = Depends(deps.get_db),
    *,
    current_user=Depends(deps.get_current_user),
    tag_in: schemas.TagCreate
):
    """
    Create new tag
    """
    tag = crud.tag.create(db, obj_in=tag_in)
    return tag


@router.put("/{tag_id}", response_model=schemas.Tag)
def update_tag(
    db: Session = Depends(deps.get_db),
    *,
    tag_id: int,
    tag_in: schemas.TagUpdate
):
    """
    Update Tag
    """
    tag = crud.tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = crud.tag.update(db, db_obj=tag, obj_in=tag_in)
    return tag


@router.delete("/{tag_id}", response_model=schemas.Tag)
def delete_tag(
    db: Session = Depends(deps.get_db),
    *,
    tag_id: int,
):
    "Delete Tag"
    tag = crud.tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = crud.tag.delete(db, id=tag_id)
    return tag
