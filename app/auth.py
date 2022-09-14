import base64
import hashlib
import os

from datetime import datetime, timedelta
from secrets import compare_digest
from typing import Union

from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.database.models import User
from app.database.schemas import TokenData

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def hash_password(password: str) -> str:
    """
    Hash incoming password and return hashed password.
    :param password:
    :return:
    """
    secret = hashlib.sha256(SECRET_KEY.encode()).digest()
    secret = base64.urlsafe_b64encode(secret)
    hashed_password = hashlib.sha512(secret + password.encode()).hexdigest()
    return hashed_password


async def authenticate_user(username: str, password: str) -> Union[User, bool]:
    """
    Check is user with a pair of username and password exists.
    :param username:
    :param password:
    :return:
    """
    user_ = User.objects.filter(username=username)
    if not user_:
        return False
    user_ = await user_.get()
    hashed_password = await hash_password(password)
    if not compare_digest(hashed_password, user_.password):
        return False
    return user_


async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create access token.
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Security(oauth2_scheme)) -> Union[User, HTTPException]:
    """
    Get user from token.
    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = User.objects.filter(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user.get()
