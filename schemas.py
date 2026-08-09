from pydantic import (
    BaseModel, # Base class all models inherit
      ConfigDict,  # Modern model configuration
        Field, # Allows defining certain constraints.
        EmailStr
      )
from typing import Annotated

from enum import Enum


class UserRole(int, Enum):
    """Permission levels available to users of the Waste2Value platform."""

    # A normal site user who can manage their own account and addresses.
    REGULAR = 1

    # An operational worker, such as a waste-collection driver.
    ADMIN = 2

    # A trusted supervisor who can manage operational activities.
    SUPER_USER = 3

    # The site owner or highest-trust administrator.
    MEGA_USER = 4

    @property
    def description(self) -> str:
        """Return a human-readable explanation of this permission level."""
        descriptions = {
            UserRole.REGULAR: "Regular user who manages their own account and addresses.",
            UserRole.ADMIN: "Operational worker, such as a waste-collection driver.",
            UserRole.SUPER_USER: "Trusted supervisor who manages operational activities.",
            UserRole.MEGA_USER: "Site owner with the highest level of administrative access.",
        }
        return descriptions[self]

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

