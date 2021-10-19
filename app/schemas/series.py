from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from .publisher import Publisher
from .author import Author
from .genre import Genre
from .tag import Tag

# Shared properties
class SeriesBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = "/na.png"
    thumbnail_image: Optional[str] = None
    is_completed: Optional[bool] = False
    publisher_id: Optional[int] = 0
    author_id: Optional[List[int]] = []
    genre_id: Optional[List[int]] = []
    tag_id: Optional[List[int]] = []

# Properties to receive on creation
class SeriesCreate(SeriesBase):
    title: str
    description: str
    thumbnail_image: str
    is_complete: str

# Properties to receive on update
class SeriesUpdate(SeriesBase):
    pass

# Properties shared by models stored in DB
class SeriesInDBBase(SeriesBase):
    id: int
    
    title: str
    description: str
    thumbnail_url: str
    is_complete: str

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Properties to return to client
class Series(SeriesInDBBase):
    publisher: Publisher = None
    author: List[Author] = []
    genre: List[Genre] = []
    tag: List[Tag] = []

# Properties properties stored in DB
class SeriesInDB(SeriesInDBBase):
    publisher_id: int