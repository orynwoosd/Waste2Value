from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models
from datetime import timedelta, datetime, UTC
from config import settings
import jwt
from jwt.exceptions import InvalidTokenError

password_hash = PasswordHash.recommended()
# oauth2_scheme =

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    try:
        return password_hash.verify(plain_password, hashed_password)

    except Exception as e:
        return False

async def authenticate_user(db: AsyncSession, username: str, password: str) -> models.User | None:
    result = await db.execute(
        select(models.User).where(models.User.phonenumber == username)
    )

    user = result.scalars().first()

    if not user:
        verify_password(password, "thtjjtjgjg imgipmtimt")
        return None
    if not verify_password(password, user.password):
        return None

    return user


def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
    data_to_ecode = data.copy()

    if expire_delta:
        expire = datetime.now(UTC) + expire_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

    data_to_ecode.update({"exp": expire})

    encode_jwt = jwt.encode(
        data_to_ecode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm
    )

    return encode_jwt


def decode_access_token(token: str) -> str | None:

    try:
        payload = jwt.decode(
            token,
              settings.secret_key.get_secret_value(),
                algorithms=[settings.algorithm], 
                options={"require": ["exp", "sub"]}
                )
        return payload.get("sub")
    
    except InvalidTokenError:
        # print("not found")
        # let errors be handled in one place
        return None
