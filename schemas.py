from pydantic import (
    BaseModel, # Base class all models inherit
      ConfigDict,  # Modern model configuration
        Field, # Allows defining certain constraints.
        EmailStr
      )
from typing import Annotated

from enum import Enum


class UserRole(int, Enum):
    REGULAR = 1
    ADMIN = 2
    SUPER_USER = 3
    MEGA_USER = 4

class BaseUserValidation(BaseModel):
    firstname: str =Field(min_length=1, max_length=100)
    lastname: str =Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=100)
    phonenumber: str


class CreateUserValidation(BaseUserValidation):
    password: str = Field(min_length=8)


class UserPublicResponse(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    model_config = ConfigDict(from_attributes=True)
    id: int
    firstname: str
    image_file: str | None
    image_path: str
    role: UserRole = Field(default=UserRole.REGULAR)
    

class UserPrivateResponse(UserPublicResponse):
    # model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    phonenumber: str

class UpdateUser(BaseModel):
    email: EmailStr | None = Field(default=None, max_length=120)
    phonenumber: str | None = Field(default=None, max_length=20, min_length=9)


class AddressResponse(BaseModel):
    id: int
    quater: str
    street_address: str | None
    nearest_landmark: str | None
    inhabitant: UserPrivateResponse

    model_config = ConfigDict(from_attributes=True)

