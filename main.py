from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends, HTTPException
from database import engine, get_db
from schemas import (
    UserPrivateResponse, CreateUserValidation,
    UpdateUser
    )
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
import models
from sqlalchemy import select, func 
from fastapi.security import OAuth2PasswordRequestForm
from auth import hash_password, authenticate_user, create_access_token
import jwt 
from datetime import datetime, timedelta
from config import settings
from fastapi.responses import JSONResponse
from dependecies import CurrentUser


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    async databse creation
    """
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan) 


@app.get("/")
async def home():
    return {"WLCM": "wlcm"}


@app.post("/users", response_model=UserPrivateResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_info: CreateUserValidation, db: Annotated[AsyncSession, Depends(get_db)]):

    def raise_exception(details: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=details
        )
    
    result = await db.execute(
        select(models.User).where(func.lower(models.User.username) == user_info.username.lower())
    )

    existing_user = result.scalars().first()
    if existing_user:
        raise raise_exception("username already exist")

    result = await db.execute(
        select(models.User).where(func.lower(models.User.email) == user_info.email.lower())
    )

    existing_email = result.scalars().first()
    if existing_email:
        raise raise_exception("email already exist")

    result = await db.execute(
        select(models.User).where(models.User.phonenumber == user_info.phonenumber)
    )

    existing_phonenumber = result.scalars().first()

    if existing_phonenumber:
        raise raise_exception("phone_number already exist ")

    hashed_password = hash_password(user_info.password)
    new_user = models.User(
        username=user_info.username,
        email=user_info.email,
        password=hashed_password,
        phonenumber=user_info.phonenumber

    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@app.patch("/users/{user_id}", response_model=UserPrivateResponse)
async def update_user(user_id: int, user_info: UpdateUser, db: Annotated[AsyncSession, Depends(get_db)]):
    # if user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         details="Not authorized to update this user"
    #     )

    def raise_exception(details: str) -> HTTPException:
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
            detail="User dose not exist"
        )

    

    if user_info.username is not None and user_info.username.lower() != user.username:
        result = await db.execute(
            select(models.User).where(func.lower(models.User.username) == user_info.username.lower())
        )
        existing_username = result.scalars().first()
        if existing_username:
            raise raise_exception("Username already exist ")

    if user_info.email is not None and user_info.email != user.email:
        result = await db.execute(
            select(models.User).where(func.lower(models.User.email) == user_info.email.lower())
        )

        existing_email = result.scalars().first()
        if existing_email:
            raise raise_exception("Email already registered")

    if user_info.phonenumber is not None and user_info.phonenumber != user.phonenumber:
        result = await db.execute(
            select(models.User).where(models.User.phonenumber == user_info.phonenumber)
        )

        existing_phonenumber = result.scalars().first()
        if existing_phonenumber:
            raise raise_exception("Phone number already registered")

    if user_info.username is not None:
        user.username = user_info.username
    
    if user_info.email is not None:
        user.email = user_info.email
    
    if user_info.phonenumber is not None:
        user.phonenumber = user_info.phonenumber

    await db.commit()
    await db.refresh(user)
    return user
    
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    # if current_user.id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to delete this user"
    #     )
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

    # if old_file:
    #     delete_profile_image(old_file)


@app.get("/users", response_model=List[UserPrivateResponse])
async def get_all_users(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User)
    )

    users = result.scalars().all()

    return users

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
async def get_current_user(current_user: CurrentUser):
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


