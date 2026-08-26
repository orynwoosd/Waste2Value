from pydantic import BaseModel, Field
from fastapi import Form
from datetime import date, datetime
from schemas import ProfileType

class AddressForm(BaseModel):
    quater: str = Field(max_length=100)
    street_address: str | None = Field(max_length=100, default=None)
    nearest_landmark: str | None = Field(max_length=100, default=None)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


    @classmethod
    def as_form(
        cls, quater: str = Form(...), 
        street_address: str | None = Form(None),
        nearest_landmark: str | None = Form(None),
        latitude: float | None = Form(None),
        longitude: float | None = Form(None),
        ):
        return cls(quater=quater, street_address=street_address, nearest_landmark=nearest_landmark, latitude=latitude, longitude=longitude)


class PickupForm(BaseModel):
    """Form helper for pickup creation from HTML forms.

    `category_id` accepts either an integer id or a category name string
    (e.g. "Biodegradable"). This keeps the API resilient when the
    frontend sends names instead of numeric ids.
    """

    category_id: int | str
    pickup_date: datetime
    time_slot: str
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @classmethod
    def as_form(
        cls,
        category_id: str = Form(...),
        pickup_date: datetime = Form(...),
        time_slot: str = Form(...),
        latitude: float | None = Form(None),
        longitude: float | None = Form(None),
    ):
        # HTML form values are strings; accept them and let the
        # endpoint interpret whether it's a numeric id or a name.
        return cls(category_id=category_id, pickup_date=pickup_date, time_slot=time_slot, latitude=latitude, longitude=longitude)


class PickupUpdateForm(BaseModel):
    """Optional fields accepted when updating a pickup."""

    category_id: int | str | None = Field(default=None)
    pickup_date: date | None = Field(default=None)
    time_slot: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)

    @classmethod
    def as_form(
        cls,
        category_id: str | None = Form(None),
        pickup_date: date | None = Form(None),
        time_slot: str | None = Form(None),
        longitude: float | None = Form(None),
        latitude: float | None = Form(None)

    ):
        values = {
            key: value
            for key, value in {
                "category_id": category_id,
                "pickup_date": pickup_date,
                "time_slot": time_slot,
                "longitude": longitude,
                "latitude": latitude,
            }.items()
            if value is not None and value != ""
        }
        return cls(**values)


class ProfileForm(BaseModel):
    """Optional fields accepted when updating a user profile."""

    profile_type: ProfileType | None = Field(default=None)
    display_name: str | None = Field(default=None, max_length=200)
    profession: str | None = Field(default=None, max_length=100)
    company_name: str | None = Field(default=None, max_length=150)
    website: str | None = Field(default=None, max_length=255)
    biography: str | None = Field(default=None)

    @classmethod
    def as_form(
        cls,
        profile_type: ProfileType | None = Form(None),
        display_name: str | None = Form(None),
        profession: str | None = Form(None),
        company_name: str | None = Form(None),
        website: str | None = Form(None),
        biography: str | None = Form(None),
    ):
        values = {
            key: value
            for key, value in {
                "profile_type": profile_type,
                "display_name": display_name,
                "profession": profession,
                "company_name": company_name,
                "website": website,
                "biography": biography,
            }.items()
            if value is not None and value != ""
        }
        return cls(**values)
    