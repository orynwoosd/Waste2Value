from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from database import get_db
from auth import decode_access_token
import models
from sqlalchemy import select, func

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_current_user(
        request: Request,
        db: Annotated[AsyncSession, Depends(get_db)],
        # token: Annotated[str | None, Security(oauth2_scheme)] = None,
) -> models.User:
    
    # if token is None:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: missing access_token cookie",
            headers={"WWW-Authenticate": "Bearer"},
        )


    if token and token.startswith("Bearer "):
        token = token[7:]
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        username_str = str(username).lower()
     
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(
        select(models.User).where(models.User.phonenumber == username_str)
    )

    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user 

CurrentUser = Annotated[models.User, Depends(get_current_user)]



# const res = await fetch("/me", {
#   method: "GET",
#   credentials: "include",  // This tells browser to send cookies
# });
