from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import func, Boolean, String, Integer, text, ForeignKey
from datetime import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base



class User(Base):
    """
    User represents anyone on the platform
    - From 
        - waste producer,
        - waste collector
        - admin
        - a regular visitor
    """
    
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(100),  nullable=False, server_default="unknown")
    lastname: Mapped[str] = mapped_column(String(100), nullable=False, server_default="unknown")
    phonenumber: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)
    address_data = relationship("AddressData", back_populates="inhabitant")

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_imgs/{self.image_file}"
        return "/static/profile_pics/default.jpg"


class AddressData(Base):
    __tablename__ = "addressdata"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    quater: Mapped[int] = mapped_column(String(100), nullable=False)
    street_address: Mapped[str] = mapped_column(String(100), nullable=True)
    Nearest_landmark: Mapped[str] = mapped_column(String(100), nullable=True)
    inhabitant_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    inhabitant = relationship(User, back_populates="address_data")
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)


    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/landmark_imgs/{self.image_file}"
        return "/static/location_img/default.jpg"

    


# class WasteCategory(Base):
#     """"""
    

# class Waste:
#     """sqlalchemy ORM for holding waste details including and each instance belong to a category"""
#     pass

# class Pickup:
#     """An sqlalchemy ORM for each pickup event of dirt made by a company."""
#     pass
# class WasteGenerator:
#     """An sqlalchemy model for each user or person producing dirt, 
#     the are the pones who produce waste. e.g, restuarant, shop, bar.
#     the place pickup requests."""
#     pass

# class WasteCollector:
#     """An sqlalchemy model for each waste collection company or worker
#     who collects waste e.g city sanitization workers. The do pickups."""
#     pass

# class Order:
#     """An sqlalchemy ORM for the purchased of products from recycled waste.
#     e.g., recycled plastic, compost soil."""
#     pass

# class 