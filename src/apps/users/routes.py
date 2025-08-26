from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Body
from jose import jwt
from loguru import logger
from pydantic import BaseModel
from pydantic.type_adapter import R
from core.security.password import Password
from settings import environment
from tortoise.exceptions import DoesNotExist
from .models import User

router = APIRouter(tags=["Users"])


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,  # Set default value as None
) -> str:
    to_encode = data.copy()
    # If expires_delta is not provided, use value from SETTINGS
    if expires_delta is None:
        expires_delta = timedelta(minutes=environment.jwt_expire_minutes)

    # Calculate token expiration time
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})

    # Encode data to JWT
    return jwt.encode(
        to_encode, environment.secret_key, algorithm=environment.security_algorithm
    )


async def authenticate_user(
    username: str,
    password: str,
) -> User | None:
    try:
        user = await User.get(username=username)
        if Password.is_valid(password, user.password, environment.secret_key):
            return user
    except DoesNotExist:
        return None


@router.post("/token", response_model=Token, summary="Get access token")
async def login_for_access_token(form_data: Login = Body()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
