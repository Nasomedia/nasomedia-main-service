from typing import Optional
from pydantic import BaseModel

# Shared properties
class SeriesTagBase(BaseModel):
    series_id: Optional[int] = None
    tag_id: Optional[int] = None

# Properties to receive on creation
class SeriesTagCreate(SeriesTagBase):
    series_id: int
    tag_id: int

# Properties to receive on update
class SeriesTagUpdate(SeriesTagBase):
    pass

# Properties shared by models stored in DB
class SeriesTagInDBBase(SeriesTagBase):
    id: int
    
    series_id: int
    tag_id: int

    class Config:
        orm_mode = True

# Properties to return to client
class SeriesTag(SeriesTagInDBBase):
    pass

# Properties properties stored in DB
class SeriesTagInDB(SeriesTagInDBBase):
    pass