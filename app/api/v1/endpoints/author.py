from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session


from app import crud, schemas, models
from app.api.v1 import deps

router = APIRouter()

@router.get("", response_model=List[schemas.Author])
def read_authors(
    db: Session = Depends(deps.get_db),
    *,
    keyword: Optional[str] = Query(
        None,
        title="검색 키워드"
    ),
):
    """
    Retrieve author
    """
    authors = crud.author.get_multi(
        db, keyword=keyword
    )
    
    return authors


@router.post("", response_model=schemas.Author)
def create_author(
    db: Session = Depends(deps.get_db),
    *,
    author_in: schemas.AuthorCreate
):
    """
    Create new author
    """
    author = crud.author.create(db=db, obj_in=author_in)
    return author


@router.put("/{author_id}", response_model=schemas.Author)
def update_author(
    db: Session = Depends(deps.get_db),
    *,
    author_id: int,
    author_in: schemas.AuthorUpdate
):
    """
    Update author
    """
    author = crud.author.get(db=db, id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    author = crud.author.update(db=db, obj_in=author_in)
    return author


@router.delete("/{author_id}", response_model=schemas.Author)
def delete_author(
    db: Session = Depends(deps.get_db),
    *,
    author_id: int,
):
    author = crud.author.get(db=db, id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    author = crud.author.remove(db=db, id=author_id)
    return author
