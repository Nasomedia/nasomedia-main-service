from typing import Optional
from pydantic import BaseModel

# Shared properties
class PublihserBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    profile_url: Optional[str] = None
    profile_image: Optional[str] = None

# Properties to receive on creation
class PublihserCreate(PublihserBase):
    name: str

# Properties to receive on update
class PublihserUpdate(PublihserBase):
    pass

# Properties shared by models stored in DB
class PublihserInDBBase(PublihserBase):
    id: int
    
    name: str
    description: str
    profile_url: str

    class Config:
        orm_mode = True

# Properties to return to client
class Publihser(PublihserInDBBase):
    pass

# Properties properties stored in DB
class PublihserInDB(PublihserInDBBase):
    pass