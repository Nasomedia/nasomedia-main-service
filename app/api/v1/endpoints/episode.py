from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Query, Path
from sqlalchemy.orm import Session

from app.core.config import settings
from app import crud, schemas, models, deps

import uuid

router = APIRouter()


@router.get("", response_model=List[schemas.Episode])
def read_episodes(
    db: Session = Depends(deps.get_db),
    *,
    desc: Optional[bool] = Query(
        True,
        title="내림차순 유무"
    ),
    series_id: int = Query(
        ...,
        title="시리즈 아이디"
    )
):
    """
    Retrieve series
    """
    response : List[schemas.Episode] = []
    episodes = crud.episode.get_multi_with_series(db, series_id=series_id, desc=desc)
    
    # 모든 series의 출판사, 작가, 장르, 태그 정보 수집
    for episode in episodes:
        episode_data = jsonable_encoder(episode)    
        response.append(schemas.Episode(**episode_data))

    return response


@router.post("", response_model=schemas.Episode)
async def create_episode(
    db: Session = Depends(deps.get_db),
    blob_service: deps.AzureBlobService = Depends(deps.AzureBlobService),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    episode_in: schemas.EpisodeCreate = Depends(schemas.EpisodeCreate.as_form)
):
    """
    Create new series
    """
    
    # 썸네일의 url 생성 및 업로드, 속성 삭제
    filename = str(uuid.uuid1())
    await blob_service.upload_file(filename=filename, file_in=episode_in.thumbnail_image)
    episode_in.__setattr__("thumbnail_url", settings.BLOB_URL+filename)
    episode_in.__delattr__("thumbnail_image")
    
    # 에피소드 생성
    episode = crud.episode.create_with_series(db, obj_in=episode_in)
    return episode


@router.put("/{episode_id}", response_model=schemas.Episode)
async def update_episode(
    db: Session = Depends(deps.get_db),
    blob_service: deps.AzureBlobService = Depends(deps.AzureBlobService),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    episode_id: int = Path(..., ge=1),
    episode_in: schemas.EpisodeUpdate = Depends(schemas.EpisodeUpdate.as_form)
):
    # 해당 id의 시리즈 수집
    episode = crud.episode.get(db, id=episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    # 썸네일 업데이트
    if getattr(episode_in, "thumbnail_image", False):
        filename = str(uuid.uuid1())
        await blob_service.upload_file(filename=filename, file_in=episode_in.thumbnail_image)
        episode_in.__setattr__("thumbnail_url", settings.BLOB_URL+filename)
        episode_in.__delattr__("thumbnail_image")

    # 시리즈 업데이트
    episode = crud.episode.update(db, db_obj=episode, obj_in=episode_in)
    return episode

@router.delete("/{episode_id}", response_model=schemas.Episode)
def delete_episode(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    episode_id: int = Path(..., ge=1)
):
    episode = crud.episode.get(db, id=episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    episode = crud.episode.delete(db,id=episode_id)
    return episode