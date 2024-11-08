from pydantic import BaseModel, ConfigDict

class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    username: str

class UserLoginDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str
    