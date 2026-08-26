from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends, HTTPException, File, UploadFile
from fastapi import Form, Body
from database import engine, get_db
from schemas import (
    UserPrivateResponse, CreateUserValidation,
    UpdateUser, AddressResponse, UserRole
    )
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
import models
from sqlalchemy import select, func 
from fastapi.security import OAuth2PasswordRequestForm
from auth import hash_password, authenticate_user, create_access_token
from datetime import timedelta
from config import settings
from fastapi.responses import JSONResponse
from dependecies import CurrentUser, required_permission_level
from fastapi.middleware.cors import CORSMiddleware
from forms import AddressForm, ProfileForm, PickupForm, PickupUpdateForm
from PIL import UnidentifiedImageError
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool
from sqlalchemy.orm import joinedload
from image_utils import process_image, delete_img
from schemas import (
    CreatePickupValidation,
    PickupResponse,
    WasteCategoryResponse,
    WasteResponse,
    UserProfileResponse
)
from schemas import (
    RoleChangeRequestCreate,
    RoleChangeRequestResponse,
    AuditLogResponse,
)
from datetime import date as _date
from datetime import datetime
from datetime import timezone, timedelta
from math import radians, sin, cos, asin, sqrt
from schemas import CollectorLocationUpdate

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    async databse creation
    """
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan) 


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # adjust to your React port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")


def _distance_km(latitude_a: float, longitude_a: float, latitude_b: float, longitude_b: float) -> float:
    earth_radius_km = 6371.0
    delta_latitude = radians(latitude_b - latitude_a)
    delta_longitude = radians(longitude_b - longitude_a)
    value = sin(delta_latitude / 2) ** 2 + cos(radians(latitude_a)) * cos(radians(latitude_b)) * sin(delta_longitude / 2) ** 2
    return 2 * earth_radius_km * asin(sqrt(min(1.0, value)))


async def _nearest_collector(db: AsyncSession, latitude: float | None, longitude: float | None, requester_id: int):
    if latitude is None or longitude is None:
        return None

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=30)
    result = await db.execute(
        select(
            models.User.id,
            models.User.last_latitude,
            models.User.last_longitude,
        ).where(
            models.User.id != requester_id,
            models.User.role == UserRole.ADMIN.name,
            models.User.is_available.is_(True),
            models.User.last_latitude.is_not(None),
            models.User.last_longitude.is_not(None),
            models.User.location_updated_at >= cutoff,
        )
    )
    collectors = result.mappings().all()
    nearest = min(
        collectors,
        key=lambda collector: _distance_km(
            latitude,
            longitude,
            collector["last_latitude"],
            collector["last_longitude"],
        ),
        default=None,
    )
    return nearest["id"] if nearest else None


@app.get("/")
async def home():
    return {"WLCM": "wlcm"}


@app.post("/users", response_model=UserPrivateResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_info: CreateUserValidation, db: Annotated[AsyncSession, Depends(get_db)]):
    """
    - This route registers a new user to the database and log them in.
    - It logs them in by creating their access token and saving it to cokie.
    """

    def _raise_exception(details: str) -> HTTPException:
        """
        A helper function for rasing exceptions.
        """
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=details
        )
    

    result = await db.execute(
        select(models.User).where(func.lower(models.User.email) == user_info.email.lower())
    )

    existing_email = result.scalars().first()
    if existing_email:
        raise _raise_exception("email already exist")

    result = await db.execute(
        select(models.User).where(models.User.phonenumber == user_info.phonenumber)
    )

    existing_phonenumber = result.scalars().first()

    if existing_phonenumber:
        raise _raise_exception("phone number already exist ")

    hashed_password = hash_password(user_info.password)
    new_user = models.User(
        firstname=user_info.firstname,
        lastname=user_info.lastname,
        email=user_info.email,
        password=hashed_password,
        phonenumber=user_info.phonenumber

    )
    new_user.create_profile()

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    
    # of authentication process.
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": new_user.phonenumber},
        expire_delta=access_token_expires,

    )

    response = JSONResponse(
        content={
            "user": UserPrivateResponse.model_validate(new_user).model_dump(),
            "token_type": "bearer",
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )

    return response


@app.post("/address", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def add_user_address(
     current_user: CurrentUser,
    address: AddressForm = Depends(AddressForm.as_form),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    
): 
    result = await db.execute(
        select(models.AddressData).options(joinedload(models.AddressData.inhabitant)).where(models.AddressData.inhabitant_id == current_user.id)
    )
    existing_address = result.scalars().first()
    if existing_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have and address."
        )
  
    file_content = await file.read()

    if len(file_content) > settings.max_upload_file_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {settings.max_upload_file_size_bytes}Mb"
        )

    try:
        # Run in threadpool to prevent blocking.
        new_file = await run_in_threadpool(process_image, file_content, "lm")
    except UnidentifiedImageError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file. Please upload a valid image (JPEG, PNG, GIF, WebP)."
        ) from err
    # debug: show parsed form fields (avoid unpacking into print)
    print(address.model_dump())
    user_new_address = models.AddressData(
        inhabitant_id=current_user.id,
        **address.model_dump()
    )
    user_new_address.image_file = new_file
    db.add(user_new_address)
    await db.commit()
    await db.refresh(user_new_address)

    # only register page has been built so nothing 
    return user_new_address


@app.patch("/collectors/me/location")
async def update_collector_location(
    location: CollectorLocationUpdate,
    current_user: Annotated[models.User, Depends(required_permission_level(UserRole.ADMIN.value))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    current_user.last_latitude = location.latitude
    current_user.last_longitude = location.longitude
    current_user.location_updated_at = datetime.now(timezone.utc)
    current_user.is_available = location.is_available
    await db.commit()
    return {"message": "Collector location updated", "is_available": current_user.is_available}
    

@app.patch("/users/{user_id}", response_model=UserPrivateResponse)
async def update_user(user_id: int, current_user: CurrentUser, user_info: UpdateUser, db: Annotated[AsyncSession, Depends(get_db)]):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    def _raise_exception(details: str) -> HTTPException:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=details
            )

    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    

    if user_info.email is not None and user_info.email != user.email:
        result = await db.execute(
            select(models.User).where(func.lower(models.User.email) == user_info.email.lower())
        )

        existing_email = result.scalars().first()
        if existing_email:
            raise _raise_exception("Email already registered")

    if user_info.phonenumber is not None and user_info.phonenumber != user.phonenumber:
        result = await db.execute(
            select(models.User).where(models.User.phonenumber == user_info.phonenumber)
        )

        existing_phonenumber = result.scalars().first()
        if existing_phonenumber:
            raise _raise_exception("Phone number already registered")

   
    if user_info.email is not None:
        user.email = user_info.email
    
    if user_info.phonenumber is not None:
        user.phonenumber = user_info.phonenumber

    await db.commit()
    await db.refresh(user)
    return user

    
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )

    existing_user = result.scalars().first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User deos not exist"
        )

    old_file = existing_user.image_file

    await db.delete(existing_user)
    await db.commit()

    if old_file:
        delete_img(old_file, type="pf")


@app.get("/users", response_model=List[UserPrivateResponse], description='This route needs MEGA_USER status to access.')
async def get_all_users(
    db: Annotated[AsyncSession, Depends(get_db)], 
    current_user: Annotated[
        models.User,
        Depends(required_permission_level(UserRole.MEGA_USER.value))
    ]
    ):
    result = await db.execute(
        select(models.User)
    )
 
    users = result.scalars().all()

    return users

@app.get("/address", response_model=List[AddressResponse])
async def get_all_addresses(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.AddressData).options(joinedload(models.AddressData.inhabitant))
    )

    addresses = result.scalars().all()
    return addresses


@app.get("/waste/categories", response_model=List[WasteCategoryResponse])
async def list_waste_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    """List available waste categories for the frontend selector.

    This returns the canonical categories seeded by migrations.
    """
    result = await db.execute(select(models.WasteCategory).order_by(models.WasteCategory.id))
    rows = result.scalars().all()
    return rows

@app.get("/waste", response_model=List[WasteResponse])
async def list_waste(db: Annotated[AsyncSession, Depends(get_db)]):
    """List all waste available"""
    result = await db.execute(
        select(models.Waste).options(
            joinedload(models.Waste.category),
            joinedload(models.Waste.producer),
        )
    )
    wastes = result.scalars().all()
    return wastes


@app.post("/role-requests", response_model=RoleChangeRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_role_request(
    current_user: CurrentUser,
     db: Annotated[AsyncSession, Depends(get_db)],
    requested_role: str = Form(...),
    file: UploadFile | None = File(None)   
):
    """Create a role change request. Users cannot self-assign roles.

    Optionally accepts a supporting document upload.
    """
    # Validate requested role
    try:
        # Accept either numeric or name values
        if requested_role.isdigit():
            requested_role_val = models.UserRole(int(requested_role))
        else:
            requested_role_val = models.UserRole[requested_role]
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid requested role")

    # Prevent downgrades or self-assignment of equal/higher privileges
    if requested_role_val.value <= current_user.role.value:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Requested role must be higher than current role")

    # Ensure there is no existing pending request
    result = await db.execute(
        select(models.RoleChangeRequest).where(
            models.RoleChangeRequest.user_id == current_user.id,
            models.RoleChangeRequest.status == models.RoleRequestStatus.PENDING,
        )
    )
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already have a pending role request")

    document_filename = None
    if file is not None:
        file_content = await file.read()
        if len(file_content) > settings.max_upload_file_size_bytes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")
        # reuse existing image processing path; documents will be saved as images if provided
        document_filename = await run_in_threadpool(process_image, file_content, "id")

    new_req = models.RoleChangeRequest(
        user_id=current_user.id,
        requested_role=requested_role_val,
        status=models.RoleRequestStatus.PENDING,
        document_filename=document_filename,
    )
    db.add(new_req)
    await db.commit()
    await db.refresh(new_req)

    return new_req


@app.get("/admin/role-requests", response_model=List[RoleChangeRequestResponse])
async def list_role_requests(
    db: Annotated[AsyncSession, Depends(get_db)],
    # current_user: CurrentUser

    current_user: Annotated[models.User, Depends(required_permission_level(models.UserRole.SUPER_USER.value))],
):
    """Admin-only view of pending role requests."""
    result = await db.execute(
        select(models.RoleChangeRequest).options(joinedload(models.RoleChangeRequest.user)).where(models.RoleChangeRequest.status == models.RoleRequestStatus.PENDING)
    )
    rows = result.scalars().all()
    return rows


@app.patch("/admin/role-requests/{request_id}", response_model=RoleChangeRequestResponse)
async def review_role_request(
    request_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(required_permission_level(models.UserRole.SUPER_USER.value))],
    action: str = Body(...),
    admin_notes: str | None = Body(None),
):
    """Approve or reject a pending role change request (admin only)."""
    result = await db.execute(select(models.RoleChangeRequest).options(
        joinedload(models.RoleChangeRequest.admin),
        joinedload(models.RoleChangeRequest.user)
        ).where(models.RoleChangeRequest.id == request_id))
    req = result.scalars().first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role request not found")
    if req.status != models.RoleRequestStatus.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request already reviewed")

    # Apply the chosen action
    if action.lower() == "approve":
        # update user role and mark request approved
        user_result = await db.execute(select(models.User).where(models.User.id == req.user_id))
        user = user_result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requesting user not found")
        user.role = req.requested_role
        req.status = models.RoleRequestStatus.APPROVED
        req.admin_id = current_user.id
        req.admin_notes = admin_notes
        req.reviewed_at = datetime.utcnow()

        log = models.AuditLog(actor_id=current_user.id, target_user_id=user.id, action="ROLE_APPROVED", details=admin_notes)
        db.add(log)

    elif action.lower() == "reject":
        req.status = models.RoleRequestStatus.REJECTED
        req.admin_id = current_user.id
        req.admin_notes = admin_notes
        req.reviewed_at = datetime.utcnow()
        log = models.AuditLog(actor_id=current_user.id, target_user_id=req.user_id, action="ROLE_REJECTED", details=admin_notes)
        db.add(log)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action; use 'approve' or 'reject'")

    await db.commit()
    await db.refresh(req)
    return req

@app.get("/pickups", response_model=List[PickupResponse], status_code=status.HTTP_200_OK)
async def get_pickups(db: Annotated[AsyncSession, Depends(get_db)]):
    """Get all schedulled pickups."""
    result = await db.execute(
        select(models.Pickup).options(joinedload(models.Pickup.waste).joinedload(models.Waste.category))
    )
    pickups = result.scalars().all()
    return pickups
    

@app.post("/pickups", response_model=PickupResponse, status_code=status.HTTP_201_CREATED)
async def create_pickup(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    form: PickupForm = Depends(PickupForm.as_form),
    file: UploadFile | None = File(None),
):
    """Create a pickup request from the frontend form.

    Workflow:
    - validate category exists
    - create a `Waste` row owned by the requester
    - process the optional image and attach filename
    - create a `Pickup` row referencing the waste item
    """
    # validate category: accept either numeric id or case-insensitive name
    cat_val = form.category_id
    category = None
    if isinstance(cat_val, int) or (isinstance(cat_val, str) and cat_val.isdigit()):
        try:
            cid = int(cat_val)
        except (TypeError, ValueError):
            cid = None
        if cid is not None:
            category = (await db.execute(
                select(models.WasteCategory).where(models.WasteCategory.id == cid)
            )).scalars().first()
    if category is None and isinstance(cat_val, str):
        category = (await db.execute(
            select(models.WasteCategory).where(func.lower(models.WasteCategory.name) == cat_val.lower())
        )).scalars().first()

    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")

    # create waste item owned by current user
    new_waste = models.Waste(category_id=category.id, producer_id=current_user.id)
    db.add(new_waste)
    await db.flush()  # populate new_waste.id

    # handle optional image upload
    image_filename = None
    if file is not None:
        file_content = await file.read()
        if len(file_content) > settings.max_upload_file_size_bytes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")
        try:
            image_filename = await run_in_threadpool(process_image, file_content, "pk")
        except UnidentifiedImageError as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file") from err

    pickup_latitude = form.latitude
    pickup_longitude = form.longitude
    if pickup_latitude is None and pickup_longitude is None:
        address_result = await db.execute(
            select(models.AddressData).where(models.AddressData.inhabitant_id == current_user.id)
        )
        saved_address = address_result.scalars().first()
        if saved_address:
            pickup_latitude = saved_address.latitude
            pickup_longitude = saved_address.longitude

    if (pickup_latitude is None) != (pickup_longitude is None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Latitude and longitude must be provided together")

    assigned_courier = await _nearest_collector(
        db, pickup_latitude, pickup_longitude, current_user.id
    )
    # create pickup record
    pickup = models.Pickup(
        waste_id=new_waste.id,
        requester_id=current_user.id,
        courier_id=assigned_courier,
        pickup_date=_date.fromisoformat(form.pickup_date) if isinstance(form.pickup_date, str) else form.pickup_date,
        time_slot=models.PickupTimeSlot(form.time_slot),
        image_file=image_filename,
        latitude=pickup_latitude,
        longitude=pickup_longitude,
        status=models.PickUpStatus.PENDING.value if assigned_courier else models.PickUpStatus.CREATED.value,
    )
    db.add(pickup)
    await db.commit()

    # Refresh and re-query with relationships eagerly loaded. In async
    # SQLAlchemy, accessing lazy relationships during FastAPI response
    # validation triggers IO which isn't allowed from the serialization
    # thread — so ensure related objects are loaded here.
    await db.refresh(pickup)
    result = await db.execute(
        select(models.Pickup)
        .options(
            joinedload(models.Pickup.waste).joinedload(models.Waste.category),
        )
        .where(models.Pickup.id == pickup.id)
    )
    pickup_with_rels = result.scalars().first()

    return pickup_with_rels


@app.patch("/pickups/{pickup_id}", response_model=PickupResponse, status_code=status.HTTP_200_OK)
async def update_pickup(
    pickup_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    form: PickupUpdateForm = Depends(PickupUpdateForm.as_form),
    file: UploadFile | None = File(None),
):
    """Update fields on a pickup that is still awaiting collection."""
    result = await db.execute(
        select(models.Pickup)
        .options(joinedload(models.Pickup.waste).joinedload(models.Waste.category))
        .where(models.Pickup.id == pickup_id)
    )
    pickup = result.scalars().first()

    if not pickup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pickup not found")
    if pickup.requester_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if pickup.status in  (models.PickUpStatus.CREATED.value, models.PickUpStatus.PENDING.value,):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only newly created pickups can be updated",
        )

    update_values = form.model_dump(exclude_unset=True)

    if "category_id" in update_values:
        category_value = update_values["category_id"]
        category = None
        if isinstance(category_value, int) or (
            isinstance(category_value, str) and category_value.isdigit()
        ):
            category = (await db.execute(
                select(models.WasteCategory).where(
                    models.WasteCategory.id == int(category_value)
                )
            )).scalars().first()
        if category is None and isinstance(category_value, str):
            category = (await db.execute(
                select(models.WasteCategory).where(
                    func.lower(models.WasteCategory.name) == category_value.lower()
                )
            )).scalars().first()
        if category is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")
        print(category)
        pickup.waste.category_id = category.id

    if "pickup_date" in update_values:
        pickup.pickup_date = update_values["pickup_date"]
    if "time_slot" in update_values:
        try:
            pickup.time_slot = models.PickupTimeSlot(update_values["time_slot"])
        except ValueError as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid time slot") from err

    old_image = pickup.image_file
    if file is not None:
        file_content = await file.read()
        if len(file_content) > settings.max_upload_file_size_bytes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")
        try:
            pickup.image_file = await run_in_threadpool(process_image, file_content, "pk")
        except UnidentifiedImageError as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file") from err

    if "longitude" in update_values:
        pickup.longitude = update_values["longitude"]

    if "latitude" in update_values:
        pickup.latitude = update_values["latitude"]
        
    await db.commit()
    await db.refresh(pickup)
    if file is not None and old_image:
        delete_img(old_image, "pk")

    result = await db.execute(
        select(models.Pickup)
        .options(joinedload(models.Pickup.waste).joinedload(models.Waste.category))
        .where(models.Pickup.id == pickup_id)
    )
    return result.scalars().first()


@app.delete("/pickups/{pickup_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pickup(
    pickup_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Delete an owned pickup that has not entered collection processing."""
    result = await db.execute(
        select(models.Pickup).where(models.Pickup.id == pickup_id)
    )
    pickup = result.scalars().first()

    if not pickup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pickup not found")
    if pickup.requester_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if pickup.status != models.PickUpStatus.CREATED.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only newly created pickups can be deleted",
        )

    old_image = pickup.image_file
    waste_result = await db.execute(
        select(func.count(models.Pickup.id)).where(models.Pickup.waste_id == pickup.waste_id)
    )
    is_only_pickup = waste_result.scalar_one() == 1
    waste = None
    if is_only_pickup:
        waste = await db.get(models.Waste, pickup.waste_id)

    await db.delete(pickup)
    if waste is not None:
        await db.delete(waste)
    await db.commit()

    if old_image:
        delete_img(old_image, "pk")


@app.get("/profiles", response_model=list[UserProfileResponse], status_code=status.HTTP_200_OK)
async def get_all_profiles(
    current_user: Annotated[models.User, Depends(required_permission_level(UserRole.SUPER_USER.value))],
    db: Annotated[AsyncSession, Depends(get_db)],

    ):
    result = await db.execute(
        select(models.Profile).options(joinedload(models.Profile.profile_owner))
    )

    profiles = result.scalars().all()
    return profiles


@app.get("/profiles/{profile_id}", response_model=UserProfileResponse, status_code=status.HTTP_200_OK)
async def get_user_profile(db: Annotated[AsyncSession, Depends(get_db)], profile_id: int):
    result = await db.execute(
        select(models.Profile).where(models.Profile.id == profile_id).options(joinedload(models.Profile.profile_owner))
        )
    user_profile = result.scalars().first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile Not found"
        )
    return user_profile

@app.patch("/profiles/{profile_id}", response_model=UserProfileResponse, status_code=status.HTTP_200_OK)
async def update_user_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    profile_id: int,
    logo: UploadFile | None = File(None),
    form: ProfileForm = Depends(ProfileForm.as_form),
):
    result = await db.execute(
        select(models.Profile).where(models.Profile.id == profile_id)
    )
    user_profile = result.scalars().first()

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )

    old_image = user_profile.logo
    if logo is not None:
        file_content = await logo.read()
        if len(file_content) > settings.max_upload_file_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="File to large"
            )
        try: 
            filename = await run_in_threadpool(process_image, file_content, "lg")
        except UnidentifiedImageError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file") from e

        user_profile.logo = filename


    for field, value in form.model_dump(exclude_unset=True).items():
        setattr(user_profile, field, value)

    await db.commit()
    await db.refresh(user_profile)

    if logo is not None and old_image:
            delete_img(old_image, "lg")
    return user_profile

@app.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(required_permission_level(UserRole.SUPER_USER.value))],
    profile_id: int
    ):

    result = await db.execute(
        select(models.Profile).where(models.Profile.id == profile_id) 
    )

    profile = result.scalars().first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    await db.delete(profile)
    await db.commit()

    if profile.logo:
        delete_img(profile.logo, "lg")

@app.post("/token")
async def login_for_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):

    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password ",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

    access_token = create_access_token(
        data={"sub": user.phonenumber}, expire_delta=access_token_expires
    )

    response = JSONResponse(
        {"access_token": access_token, "token_type": "bearer"}
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )

    return response


@app.get("/me", response_model=UserPrivateResponse)
async def get_current_user(current_user: CurrentUser ):
    """Get the currently authenticated user."""
    return current_user

@app.post("/logout")
async def logout():
    response = JSONResponse(
        {"status": "logged_out"}
    )

    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
    )

    return response


### legacy: older pickup route removed — use POST /pickups instead.
 