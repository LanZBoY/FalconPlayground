from pydantic import BaseModel, Field, ConfigDict


class BaseTagDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(None)
    name: str = Field(min_length=1)


class PostTagDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    post_id: int = Field()
    tag_id: int = Field()
