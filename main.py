from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends, HTTPException, File, UploadFile
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
from forms import AddressForm
from PIL import UnidentifiedImageError
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool
from sqlalchemy.orm import joinedload
from image_utils import process_image, delete_img

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
    # current_user: Annotated[
    #     models.User,
        # Depends(required_permission_level(UserRole.MEGA_USER.value))
    # ]
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


 