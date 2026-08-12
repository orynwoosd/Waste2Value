from pydantic import BaseModel, Field
from fastapi import Form
from datetime import datetime

class AddressForm(BaseModel):
    quater: str = Field(max_length=100)
    street_address: str | None = Field(max_length=100, default=None)
    nearest_landmark: str | None = Field(max_length=100, default=None)


    @classmethod
    def as_form(
        cls, quater: str = Form(...), 
        street_address: str | None = Form(None),
        nearest_landmark: str | None = Form(None)
        ):
        return cls(quater=quater, street_address=street_address, nearest_landmark=nearest_landmark)


class PickupForm(BaseModel):
    """Form helper for pickup creation from HTML forms.

    `category_id` accepts either an integer id or a category name string
    (e.g. "Biodegradable"). This keeps the API resilient when the
    frontend sends names instead of numeric ids.
    """

    category_id: int | str
    pickup_date: datetime
    time_slot: str

    @classmethod
    def as_form(
        cls,
        category_id: str = Form(...),
        pickup_date: datetime = Form(...),
        time_slot: str = Form(...),
    ):
        # HTML form values are strings; accept them and let the
        # endpoint interpret whether it's a numeric id or a name.
        return cls(category_id=category_id, pickup_date=pickup_date, time_slot=time_slot)