from typing import Any
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Date, String, Integer, text, ForeignKey, Enum as DBEnum, Text, JSON, Float, Boolean
from datetime import date, datetime
from enum import Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
from schemas import UserRole
import bleach
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
    last_longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    location_updated_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    address_data = relationship("AddressData", back_populates="inhabitant")
    role: Mapped[UserRole] = mapped_column(
        DBEnum(UserRole, name="userrole"),
        default=UserRole.REGULAR,
        server_default=UserRole.REGULAR.name,
    )
    

    # Relationship to wastes produced by this user
    wastes: Mapped[list["Waste"]] = relationship(
        "Waste", back_populates="producer",
        cascade="all, delete-orphan",
        foreign_keys="[Waste.producer_id]"
        )

    # Role change requests submitted by this user (one-to-many)
    role_change_requests: Mapped[list["RoleChangeRequest"]] = relationship(
        "RoleChangeRequest",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="[RoleChangeRequest.user_id]"
    )

    # Audit logs where this user acted as the actor
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="actor",
        foreign_keys="[AuditLog.actor_id]",
        cascade="all, delete-orphan",
    )

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

    profile: Mapped["Profile | None"] = relationship(
        "Profile",
        back_populates="profile_owner",
        uselist=False,
        cascade="all, delete-orphan",
        foreign_keys="[Profile.user_id]"
    )

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_imgs/{self.image_file}"
        return "/static/profile_pics/default.jpg"

    def create_profile(self) -> "Profile":
        """Create the default profile associated with this user."""
        profile = Profile(
            profile_owner=self,
            profile_type=ProfileType.INDIVIDUAL,
            profile_data={},
        )
        self.profile = profile
        return profile


class AddressData(Base):
    __tablename__ = "addressdata"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    quater: Mapped[int] = mapped_column(String(100), nullable=False)
    street_address: Mapped[str] = mapped_column(String(100), nullable=True)
    nearest_landmark: Mapped[str] = mapped_column(String(100), nullable=True)
    inhabitant_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    inhabitant = relationship(User, back_populates="address_data")
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)

    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)


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

    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_imgs/{self.image_file}"
        return "/static/profile_pics/default.jpg"



class RoleRequestStatus(str, Enum):
    """Status values for role change requests."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class RoleChangeRequest(Base):
    """A request submitted by a user asking the administrators to change their role.

    Fields:
    - `user_id`: the requesting user
    - `requested_role`: the role the user is requesting
    - `status`: current state of the request (PENDING/APPROVED/REJECTED)
    - `document_filename`: optional supporting document (e.g., business registration)
    - `admin_id`: the admin who reviewed the request
    - `admin_notes`: optional notes recorded by the reviewing admin
    - timestamps for creation and review
    """

    __tablename__ = "role_change_requests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    requested_role: Mapped[UserRole] = mapped_column(DBEnum(UserRole, name="userrole"), nullable=False)
    status: Mapped[RoleRequestStatus] = mapped_column(DBEnum(RoleRequestStatus, name="rolerequeststatus"), nullable=False, server_default=RoleRequestStatus.PENDING.value)
    document_filename: Mapped[str | None] = mapped_column(String(200), nullable=True)
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    admin_notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    reviewed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="role_change_requests", foreign_keys=[user_id])
    admin = relationship("User", foreign_keys=[admin_id])

    @property
    def image_path(self) -> str:
        if self.document_filename:
            return f"/media/profile_imgs/{self.document_filename}"
        return "/static/profile_pics/default.jpg"
    


class AuditLog(Base):
    """Simple audit trail of important actions performed by users/admins.

    We write entries when admin approves/rejects a role request so there is
    an immutable record of who did what and when.
    """

    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    actor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    target_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(200), nullable=False)
    details: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    actor = relationship("User", back_populates="audit_logs", foreign_keys=[actor_id])
    target_user = relationship("User", foreign_keys=[target_user_id])


class ProfileType(str, Enum):
    """Type of user profile carried by the account."""

    INDIVIDUAL = "individual"
    BUSINESS = "business"
    ORGANIZATION = "organization"
    COMMUNITY = "community"


class Profile(Base):
    """User profile that stores both fixed fields and flexible profile metadata."""

    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    profile_type: Mapped[ProfileType] = mapped_column(
        DBEnum(
            ProfileType,
            name="profiletype",
            values_callable=lambda enum_type: [member.value for member in enum_type],
        ),
        nullable=False,
        default=ProfileType.INDIVIDUAL,
        server_default=ProfileType.INDIVIDUAL.value,
    )
    display_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    profession: Mapped[str | None] = mapped_column(String(100), nullable=True)
    company_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    logo: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)
    biography: Mapped[str | None] = mapped_column(Text, nullable=True)
    profile_data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    profile_owner = relationship("User", back_populates="profile")

    def _set_content(self, html_str):
        allowed_tags = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'p', 'ul', 'ol', 'li', 'br',
            'strong', 'em', 'a', 'span',
            'div', 'img', 'table', 'tr', 'td'
        ]
        self.biography = bleach.clean(html_str, tags=allowed_tags)

    def get_biography(self):
        return self.biography

    def get_profile_data_value(self, key: str, default=None):
        return self.profile_data.get(key, default) if self.profile_data else default

    @property
    def image_path(self) -> str:
        if self.logo:
            return f"/media/profile_imgs/{self.logo}"
        return "/static/profile_pics/default.jpg"
    



    # ROles should be editeble form here.

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

