from fastapi import UploadFile, Form, File
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.sql.operators import is_

from .publisher import Publisher
from .author import Author
from .genre import Genre
from .tag import Tag

import ast

# Shared properties
class SeriesBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    thumbnail_image: Optional[str] = None
    is_completed: Optional[bool] = False

# Properties to receive on creation
class SeriesCreate(SeriesBase):
    title: str 
    thumbnail_image: UploadFile
    is_completed: bool

    description: Optional[str]
    publisher_id: Optional[int]
    author_id: Optional[List[int]]
    genre_id: Optional[List[int]]
    tag_id: Optional[List[int]]
    
    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        is_completed: str = Form(...),
        thumbnail_image: UploadFile = File(...),
        description: str = Form(None),
        publisher_id: int = Form(None),
        author_id: str = Form('[]'),
        genre_id: str = Form('[]'),
        tag_id: str = Form('[]'),
    ):
        is_completed = True if is_completed=="true" else False

        return cls(title=title, 
                publisher_id=publisher_id, 
                description=description, 
                thumbnail_image=thumbnail_image, 
                is_completed=is_completed,
                author_id=ast.literal_eval(author_id),
                genre_id=ast.literal_eval(genre_id),
                tag_id=ast.literal_eval(tag_id))

# Properties to receive on update
class SeriesUpdate(SeriesBase):
    publisher_id: Optional[int]
    author_id: Optional[List[int]]
    genre_id: Optional[List[int]]
    tag_id: Optional[List[int]]

    def as_form(
        cls,
        title: str = Form(None),
        is_completed: str = Form(None),
        thumbnail_image: UploadFile = File(None),
        description: str = Form(None),
        publisher_id: int = Form(None),
        author_id: Optional[List[int]] = Form('[]'),
        genre_id: Optional[List[int]] = Form('[]'),
        tag_id: Optional[List[int]] = Form('[]'),
    ):

        return cls(title=title, 
                publisher_id=publisher_id, 
                description=description, 
                thumbnail_image=thumbnail_image, 
                is_completed=is_completed,
                author_id=ast.literal_eval(author_id),
                genre_id=ast.literal_eval(genre_id),
                tag_id=ast.literal_eval(tag_id))



# Properties shared by models stored in DB
class SeriesInDBBase(SeriesBase):
    id: int
    
    title: str
    description: str
    thumbnail_url: str
    is_completed: bool

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
    thumbnail_url: str
    publisher_id: int
