from pydantic import BaseModel, ConfigDict, Field
from utils.role import UserRole


class JWTPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    user_id: int = Field(None, alias="id")
    role: UserRole = Field()


class BaseUserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AdminView_User(BaseUserModel):
    id: int = Field()
    username: str = Field(min_length=1)
    email: str = Field(
        min_length=1,
        pattern=r"^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$",
    )
    address: str = Field(min_length=1)


class OwnerView_User(BaseUserModel):
    username: str = Field(min_length=1)
    email: str = Field(
        min_length=1,
        pattern=r"^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$",
    )
    address: str = Field(min_length=1)


class UserRegisterDTO(BaseUserModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    email: str = Field(
        min_length=1,
        pattern=r"^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$",
    )
    address: str = Field(min_length=1)


class UserLoginDTO(BaseUserModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserUpdateDTO(BaseUserModel):
    email: str = Field(
        min_length=1,
        pattern=r"^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$",
    )
    address: str = Field(min_length=1)


class UserView_PostAuthor(BaseUserModel):
    id: int = Field(None)
    email: str | None = None
    username: str | None = None
