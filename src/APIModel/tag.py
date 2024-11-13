from pydantic import BaseModel, Field

class BaseTagDTO(BaseModel):
    id: int = Field(None)
    name: str = Field(min_length=1)