from typing import Optional
from pydantic import BaseModel

# Shared properties
class SeriesAuthorBase(BaseModel):
    series_id: Optional[int] = None
    author_id: Optional[int] = None

# Properties to receive on creation
class SeriesAuthorCreate(SeriesAuthorBase):
    series_id: int
    author_id: int

# Properties to receive on update
class SeriesAuthorUpdate(SeriesAuthorBase):
    pass

# Properties shared by models stored in DB
class SeriesAuthorInDBBase(SeriesAuthorBase):
    id: int
    
    series_id: int
    author_id: int

    class Config:
        orm_mode = True

# Properties to return to client
class SeriesAuthor(SeriesAuthorInDBBase):
    pass

# Properties properties stored in DB
class SeriesAuthorInDB(SeriesAuthorInDBBase):
    pass