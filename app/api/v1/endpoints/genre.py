from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session


from app import crud, schemas, models
from app.api.v1 import deps

router = APIRouter()

@router.get("", response_model=List[schemas.Genre])
def read_genre(
    db: Session = Depends(deps.get_db),
    *,
    keyword: Optional[str] = Query(
        "",
        title="검색 키워드"
    ),
):
    """
    Retrieve genre
    """
    genres = crud.genre.get_multi(
        db, keyword=keyword
    )
    return genres


@router.post("", response_model=schemas.Genre)
def create_genre(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    genre_in: schemas.GenreCreate
):
    """
    Create new genre
    """
    genre = crud.genre.create(db, obj_in=genre_in)
    return genre


@router.put("/{genre_id}", response_model=schemas.Genre)
def update_genre(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    genre_id: int,
    genre_in: schemas.GenreUpdate
):
    """
    Update Genre
    """
    genre = crud.genre.get(db, id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    genre = crud.genre.update(db, db_obj=genre, obj_in=genre_in)
    return genre


@router.delete("/{genre_id}", response_model=schemas.Genre)
def delete_genre(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    genre_id: int,
):
    "Delete Genre"
    genre = crud.genre.get(db, id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    genre = crud.genre.delete(db, id=genre_id)
    return genre
