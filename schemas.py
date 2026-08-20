from typing import Any
from pydantic import (
    BaseModel, # Base class all models inherit
      ConfigDict,  # Modern model configuration
        Field, # Allows defining certain constraints.
        EmailStr
      )

from enum import Enum
from datetime import date, datetime
import uuid


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


class WasteCategoryResponse(BaseModel):
    """Response model for a waste category."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class WasteResponse(BaseModel):
    """Response model for a waste item."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    category: WasteCategoryResponse
    producer_id: int


class CreatePickupValidation(BaseModel):
    """Validation model for creating a pickup from form fields.

    The frontend submits category, date and time-slot; an optional image
    may be uploaded separately.
    """

    # Accept either the numeric id of the category or the category name.
    category_id: int | str
    pickup_date: date
    time_slot: str


class PickupResponse(BaseModel):
    """Response model for a pickup request."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    waste: WasteResponse
    requester_id: int
    courier_id: int | None
    pickup_date: date
    time_slot: str
    status: int
    image_file: str | None
    created_at: datetime
    pickup_id: uuid.UUID
    


class RoleChangeRequestCreate(BaseModel):
    """Client payload when requesting a role change."""

    requested_role: UserRole


class RoleChangeRequestResponse(BaseModel):
    """Public response model for a RoleChangeRequest."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    requested_role: UserRole
    status: str
    document_filename: str | None
    admin_id: int | None
    admin_notes: str | None
    created_at: datetime
    reviewed_at: datetime | None
    user: UserPrivateResponse


class AuditLogResponse(BaseModel):
    """Response model for an audit log entry."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    actor_id: int
    target_user_id: int | None
    action: str
    details: str | None
    created_at: datetime


class ProfileType(str, Enum):
    INDIVIDUAL = "individual"
    BUSINESS = "business"
    ORGANIZATION = "organization"
    COMMUNITY = "community"


class UserProfile(BaseModel):
    """Represents a flexible user profile. Common fields live here; extra
    attributes can be stored in metadata for business and organisation users."""

    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    user_id: int
    profile_type: ProfileType = ProfileType.INDIVIDUAL
    display_name: str | None = None
    profession: str | None = None
    company_name: str | None = None
    website: str | None = None
    logo: str | None = None
    biography: str | None = None
    profile_data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | None = None


class UserProfileResponse(UserProfile):
    model_config = ConfigDict(from_attributes=True)
    profile_owner: UserPrivateResponse | None = None

