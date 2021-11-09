from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.params import Query, Path
from sqlalchemy.orm import Session

from app.core.config import settings

from app import crud, schemas, models
from app.api.v1 import deps

import uuid

router = APIRouter()

@router.get("/{series_id}", response_model=schemas.Series)
def read_series(
    db: Session = Depends(deps.get_db),
    *,
    series_id: int = Path(..., ge=1)
):
    series = crud.series.get(db, id=series_id)
    if not series:
        raise HTTPException(status_code=404, detail='Series not found')

    series_data = jsonable_encoder(series)
    publisher = crud.publisher.get(db, id=series.publisher_id)
    author = crud.series_author.get_authors_with_series(db, series_id=series.id)
    genre = crud.series_author.get_authors_with_series(db, series_id=series.id)
    tag = crud.series_author.get_authors_with_series(db, series_id=series.id)
    
    response = schemas.Series(**series_data, publisher=publisher, author=author, genre=genre, tag=tag)
    return response

@router.get("", response_model=List[schemas.Series])
def read_serieses(
    db: Session = Depends(deps.get_db),
    *,
    sort_by: Optional[str] = Query(
        "id",
        title="시리즈 정렬 기준",
        enum=[e.value for e in schemas.SeriesSortEnum]
    ),
    desc: Optional[bool] = Query(
        True,
        title="내림차순 유무"
    ),
    keyword: Optional[str] = Query(
        None,
        title="검색 키워드"
    ),
):
    """
    Retrieve series
    """
    response : List[schemas.Series] = []
    serieses = crud.series.get_multi(
        db, sort_by=sort_by, keyword=keyword, desc=desc
    )
    
    # 모든 series의 출판사, 작가, 장르, 태그 정보 수집
    for series in serieses:
        series_data = jsonable_encoder(series)
        publisher = crud.publisher.get(db, id=series.publisher_id)
        author = crud.series_author.get_authors_with_series(db, series_id=series.id)
        genre = crud.series_author.get_authors_with_series(db, series_id=series.id)
        tag = crud.series_author.get_authors_with_series(db, series_id=series.id)
        response.append(schemas.Series(**series_data, publisher=publisher, author=author, genre=genre, tag=tag))

    return response


@router.post("", response_model=schemas.Series)
async def create_series(
    db: Session = Depends(deps.get_db),
    blob_service: deps.AzureBlobService = Depends(deps.AzureBlobService),
    *,
    series_in: schemas.SeriesCreate = Depends(schemas.SeriesCreate.as_form)
):
    """
    Create new series
    """
    
    # 썸네일의 url 생성 및 업로드, 속성 삭제
    filename = str(uuid.uuid1())
    await blob_service.upload_file(filename=filename, file_in=series_in.thumbnail_image)
    series_in.__setattr__("thumbnail_url", settings.BLOB_URL+filename)
    series_in.__delattr__("thumbnail_image")
    
    # 시리즈와 작가, 장르, 태그 연결
    next_series_id = getattr(db.query(models.Series).order_by(-models.Series.id).first(), 'id', 0) + 1
    if getattr(series_in, "author_id", False):
        for author_id in series_in.author_id:
            crud.series_author.create(db, obj_in=schemas.SeriesAuthorCreate(series_id=next_series_id, author_id=author_id))
        delattr(series_in, "author_id")
    if getattr(series_in, "genre_id", False):
        for genre_id in series_in.genre_id:
            crud.series_genre.create(db, obj_in=schemas.SeriesAuthorCreate(series_id=next_series_id, genre_id=genre_id))
        delattr(series_in, "genre_id")
    if getattr(series_in, "tag_id", False):
        for tag_id in series_in.tag_id:
            crud.series_tag.create(db, obj_in=schemas.SeriesAuthorCreate(series_id=next_series_id, tag_id=tag_id))
        delattr(series_in, "tag_id")
    
    # 시리즈 생성
    series = crud.series.create(db, obj_in=series_in)
    series_data = jsonable_encoder(series)
    
    # response body 생성
    publisher = crud.publisher.get(db, id=series.publisher_id)
    author = crud.series_author.get_authors_with_series(db, series_id=series.id)
    genre = crud.series_genre.get_genres_with_series(db, series_id=series.id)
    tag = crud.series_tag.get_tags_with_series(db, series_id=series.id)
        
    response = schemas.Series(**series_data, publisher=publisher, author=author, genre=genre, tag=tag)
    return response


@router.put("/{series_id}", response_model=schemas.Series)
async def update_series(
    db: Session = Depends(deps.get_db),
    blob_service: deps.AzureBlobService = Depends(deps.AzureBlobService),
    *,
    series_id: int = Path(..., ge=1),
    series_in: schemas.SeriesUpdate = Depends(schemas.SeriesUpdate.as_form)
):
    # 해당 id의 시리즈 수집
    series = crud.series.get(db, id=series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")

    # 썸네일 업데이트
    if getattr(series_in, "thumbnail_image", False):
        filename = str(uuid.uuid1())
        await blob_service.upload_file(filename=filename, file_in=series_in.thumbnail_image)
        series_in.__setattr__("thumbnail_url", settings.BLOB_URL+filename)
        series_in.__delattr__("thumbnail_image")

    # 작가, 장르, 태그 업데이트
    if getattr(series_in, "author_id", False):
        for author_id in series_in.author_id:
            crud.series_author.create(db, obj_in=schemas.SeriesAuthorCreate(series_id=series_id, author_id=author_id))
        delattr(series_in, "author_id")
    if getattr(series_in, "genre_id", False):
        for genre_id in series_in.genre_id:
            crud.series_genre.create(db, obj_in=schemas.SeriesAuthorCreate(series_id=series_id, genre_id=genre_id))
        delattr(series_in, "genre_id")
    if getattr(series_in, "tag_id", False):
        for tag_id in series_in.tag_id:
            crud.series_tag.create(db, obj_in=schemas.SeriesAuthorCreate(series_id=series_id, tag_id=tag_id))
        delattr(series_in, "tag_id")

    # 시리즈 업데이트
    series = crud.series.update(db, db_obj=series, obj_in=series_in)
    series_data = jsonable_encoder(series)
    
    # response body 생성
    publisher = crud.publisher.get(db, id=series.publisher_id)
    author = crud.series_author.get_authors_with_series(db, series_id=series.id)
    genre = crud.series_genre.get_genres_with_series(db, series_id=series.id)
    tag = crud.series_tag.get_tags_with_series(db, series_id=series.id)
        
    response = schemas.Series(**series_data, publisher=publisher, author=author, genre=genre, tag=tag)
    return response

@router.delete("/{series_id}", response_model=schemas.Series)
def delete_series(
    db: Session = Depends(deps.get_db),
    *,
    series_id: int = Path(..., ge=1)
):
    series = crud.series.get(db, id=series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    
    series_data = jsonable_encoder(series)
    publisher = crud.publisher.get(db, id=series.publisher_id)
    author = crud.series_author.get_authors_with_series(db, series_id=series.id)
    genre = crud.series_genre.get_genres_with_series(db, series_id=series.id)
    tag = crud.series_tag.get_tags_with_series(db, series_id=series.id)

    crud.series.delete(db,id=series_id)

    response = schemas.Series(**series_data, publisher=publisher, author=author, genre=genre, tag=tag)
    return response