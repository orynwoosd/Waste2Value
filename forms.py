from pydantic import BaseModel, Field
from fastapi import Form, UploadFile, File

class AddressForm(BaseModel):
    quater: str = Field(max_length=100)
    street_address: str | None = Field(max_length=100, default=None)
    Nearest_landmark: str | None = Field(max_length=100, default=None)


    @classmethod
    def as_form(
        cls, quater: str = Form(...), 
        street_address: str | None = Form(None),
        Nearest_landmark: str | None = Form(None)
        ):
        return cls(quater=quater, street_address=street_address, Nearest_landmark=Nearest_landmark)