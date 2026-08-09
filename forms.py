from pydantic import BaseModel, Field
from fastapi import Form

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