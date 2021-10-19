from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class EpisodeBase(BaseModel):
    title: Optional[str] = None
    order: Optional[int] = 0
    thumbnail_url: Optional[str] = "/na.png"
    thumbnail_image: Optional[str] = None
    is_book: Optional[bool] = False
    book_id: Optional[int] = 0
    price: Optional[int] = 0
    series_id: Optional[int] = 0

# Properties to receive on creation
class EpisodeCreate(EpisodeBase):
    title: str
    order: int
    thumbnail_image: str
    is_book: bool
    book_id: int
    price: int

# Properties to receive on update
class EpisodeUpdate(EpisodeBase):
    pass

# Properties shared by models stored in DB
class EpisodeInDBBase(EpisodeBase):
    id: int
    
    title: str
    order: int
    thumbnail_url: str
    is_book: bool
    book_id: int
    price: int

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Properties to return to client
class Episode(EpisodeInDBBase):
    pass

# Properties properties stored in DB
class EpisodeInDB(EpisodeInDBBase):
    series_id: int