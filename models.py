from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Date, String, Integer, text, ForeignKey, Enum as DBEnum
from datetime import date, datetime
from enum import Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
from schemas import UserRole

from sqlalchemy.dialects.postgresql import UUID
import uuid

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
    role: Mapped[UserRole] = mapped_column(
        DBEnum(UserRole, name="userrole"),
        default=UserRole.REGULAR,
        server_default=UserRole.REGULAR.name,
    )

    # Relationship to wastes produced by this user
    wastes: Mapped[list["Waste"]] = relationship("Waste", back_populates="producer")

    # There are two FK paths between `users` and `pickups` (requester_id and
    # courier_id). Explicitly declare which foreign key each relationship
    # uses so SQLAlchemy can configure joins unambiguously.
    requested_orders: Mapped[list["Pickup"]] = relationship(
        "Pickup",
        back_populates="requester",
        foreign_keys="[Pickup.requester_id]",
    )
    courier_orders: Mapped[list["Pickup"]] = relationship(
        "Pickup",
        back_populates="courier",
        foreign_keys="[Pickup.courier_id]",
    )

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
    nearest_landmark: Mapped[str] = mapped_column(String(100), nullable=True)
    inhabitant_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    inhabitant = relationship(User, back_populates="address_data")
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)


    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/landmark_imgs/{self.image_file}"
        return "/static/location_img/default.jpg"

    


class WasteCategoryName(str, Enum):
    BIODEGRADABLE = "biodegradable"
    NON_BIODEGRADABLE = "non_biodegradable"
    MIXED = "mixed"


class PickupTimeSlot(str, Enum):
    MORNING = "morning"
    MIDDAY = "midday"
    EVENING = "evening"

class PickUpStatus(int, Enum):
        """Status of a pickup request.

        Use simple, single values for status codes so they are easy to
        compare and store. Keep semantics clear:
            - CREATED: request created by user
            - PENDING: courier assigned / in-progress
            - COMPLETED: pickup successfully collected
            - FAILED: pickup failed
            - CANCELLED: request cancelled
            - CONFLICTED: dispute between requester and courier
            - RESOLVED: disputed pickup has been resolved
        """
        CREATED = 1
        PENDING = 2
        COMPLETED = 3
        FAILED = 4
        CANCELLED = 5
        CONFLICTED = 6
        RESOLVED = 7

class WasteCategory(Base):
    """A category that can be selected when scheduling a waste pickup."""

    __tablename__ = "waste_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[WasteCategoryName] = mapped_column(
        DBEnum(WasteCategoryName, name="wastecategoryname"),
        unique=True,
        nullable=False,
    )
    wastes = relationship("Waste", back_populates="category")


class Waste(Base):
    """Waste selected for collection, belonging to one category and user."""

    __tablename__ = "wastes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("waste_categories.id"), nullable=False
    )
    producer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category = relationship("WasteCategory", back_populates="wastes")
    producer = relationship("User", back_populates="wastes")
    pickups = relationship("Pickup", back_populates="waste")


class Pickup(Base):
    """A scheduled collection of one waste item."""

    __tablename__ = "pickups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    waste_id: Mapped[int] = mapped_column(ForeignKey("wastes.id"), nullable=False)

    requester_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    courier_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)  # we dont know who it will be at creation time.

    pickup_date: Mapped[date] = mapped_column(Date, nullable=False)
    time_slot: Mapped[PickupTimeSlot] = mapped_column(
        DBEnum(PickupTimeSlot, name="pickuptimeslot"), nullable=False
    )
    status: Mapped[int] = mapped_column(
        Integer,
        default=PickUpStatus.CREATED.value,
        server_default=str(PickUpStatus.CREATED.value),
        nullable=False,
    )
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True)
    waste = relationship("Waste", back_populates="pickups")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    # Keep good trck of task when conflicts occur.
    pickup_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4) 

    requester: Mapped["User"] = relationship(
        foreign_keys=[requester_id], back_populates="requested_orders"
    )
    courier: Mapped["User"]  = relationship(
        foreign_keys=[courier_id], back_populates="courier_orders"
    )


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