from pydantic import BaseModel, ConfigDict

class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str