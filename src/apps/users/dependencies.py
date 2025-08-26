from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

from settings import environment

from .models import User


def get_credentials_exception() -> HTTPException:
    """Create credentials exception for authentication errors."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(token=Depends(HTTPBearer())) -> User:
    """
    Get current authenticated user from JWT token.

    :param token: JWT token from Authorization header
    :return: Authenticated user
    :raises: HTTPException if authentication fails
    """
    try:
        token_str = token.credentials
        payload = jwt.decode(
            token_str,
            environment.secret_key,
            algorithms=[environment.security_algorithm],
        )
        username: str = payload.get("sub")
        if username is None:
            raise get_credentials_exception()
    except JWTError:
        raise get_credentials_exception()
    user = User.get(username=username)
    if user is None:
        raise get_credentials_exception()
    return user
