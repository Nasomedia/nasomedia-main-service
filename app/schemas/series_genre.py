from typing import Optional
from pydantic import BaseModel

# Shared properties
class SeriesGenreBase(BaseModel):
    series_id: Optional[int] = None
    genre_id: Optional[int] = None

# Properties to receive on creation
class SeriesGenreCreate(SeriesGenreBase):
    series_id: int
    genre_id: int

# Properties to receive on update
class SeriesGenreUpdate(SeriesGenreBase):
    pass

# Properties shared by models stored in DB
class SeriesGenreInDBBase(SeriesGenreBase):
    id: int
    
    series_id: int
    genre_id: int

    class Config:
        orm_mode = True

# Properties to return to client
class SeriesGenre(SeriesGenreInDBBase):
    pass

# Properties properties stored in DB
class SeriesGenreInDB(SeriesGenreInDBBase):
    pass