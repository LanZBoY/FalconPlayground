from pydantic import BaseModel, ConfigDict, Field
from RequestModel import AuthorDTO
from typing import Optional

class BasePostModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : Optional[int] = None
    title : str = Field(min_length=1)
    content : str = Field(min_length=1)

class UserViewPostModel(BasePostModel):
    author : AuthorDTO

class UpdatePostModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title : str = Field(min_length=1)
    content : str = Field(min_length=1)