from pydantic import BaseModel, ConfigDict, Field
from APIModel import UserView_PostAuthor
from typing import Optional,List

class BasePostModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : Optional[int] = None
    title : str = Field(min_length=1)
    content : str = Field(min_length=1)

class UserViewListPostModel(BasePostModel):
    pass

class DetailTagDTO(BaseModel):
    id: int = Field(None)
    name: str = Field(min_length=1)

class UserViewDetailPostModel(BasePostModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    author :UserView_PostAuthor = Field(None)
    tags :List[DetailTagDTO] = Field(None)
    isOwner: bool = Field(None)

class UpdatePostModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title : str = Field(min_length=1)
    content : str = Field(min_length=1)