from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED


class AuthenticationErrorMiddleware(BaseHTTPMiddleware):
    """Middleware for handling authentication errors (401)."""

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            # Check if it's an authentication error
            if hasattr(e, "status_code") and e.status_code == HTTP_401_UNAUTHORIZED:
                logger.warning(
                    "Authentication failed for {} {}: {}",
                    request.method,
                    request.url.path,
                    str(e),
                )
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={
                        "detail": "Authentication required",
                        "error": "UNAUTHORIZED",
                        "message": "Valid authentication credentials are required to access this resource",  # noqa: E501
                    },
                )

            # Re-raise other exceptions to be handled by other middleware
            raise
