from pydantic import BaseModel, ConfigDict, Field
from APIModel import UserView_PostAuthor
from typing import Optional

class BasePostModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : Optional[int] = None
    title : str = Field(min_length=1)
    content : str = Field(min_length=1)

class UserViewListPostModel(BasePostModel):
    pass

class UserViewDetailPostModel(BasePostModel):
    isOwner: bool = Field(None)

class UpdatePostModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title : str = Field(min_length=1)
    content : str = Field(min_length=1)