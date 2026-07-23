from pydantic import (
    BaseModel, # Base class all models inherit
      ConfigDict,  # Modern model configuration
        Field, # Allows defining certain constraints.
        EmailStr
      )

from datetime import datetime

class BaseUserValidation(BaseModel):
    username: str =Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)
    phonenumber: str


class CreateUserValidation(BaseUserValidation):
    password: str = Field(min_length=8)


class UserPublicResponse(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    image_file: str | None
    image_path: str

class UserPrivateResponse(UserPublicResponse):
    # model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    phonenumber: str

class UpdateUser(BaseModel):
    username: str| None =Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    phonenumber: str | None = Field(default=None, max_length=20, min_length=9)
