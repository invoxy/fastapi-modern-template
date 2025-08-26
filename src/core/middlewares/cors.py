from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_400_BAD_REQUEST

from settings import environment


class CORSMiddleware(BaseHTTPMiddleware):
    """Middleware for handling CORS (Cross-Origin Resource Sharing)."""

    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        logger.debug(f"CORS: {request.method} {request.url.path} from {origin}")

        # Handle preflight OPTIONS requests
        if request.method == "OPTIONS":
            return await self._handle_preflight_request(request)

        # Handle regular requests
        response = await call_next(request)
        return await self._add_cors_headers(request, response)

    async def _handle_preflight_request(self, request: Request) -> JSONResponse:
        """Handles preflight OPTIONS requests for CORS."""
        origin = request.headers.get("origin")

        # Check if origin is allowed
        if not self._is_origin_allowed(origin):
            logger.warning(f"CORS: Origin not allowed: {origin}")
            return JSONResponse(
                status_code=HTTP_400_BAD_REQUEST,
                content={"detail": "Origin not allowed"},
            )

        logger.info(f"CORS: Preflight request allowed for origin: {origin}")

        # Create response with CORS headers
        response = JSONResponse(content={"detail": "OK"})
        await self._add_cors_headers(request, response)

        # Add headers for preflight
        response.headers["Access-Control-Max-Age"] = "86400"  # 24 hours

        return response

    async def _add_cors_headers(self, request: Request, response) -> JSONResponse:
        """Adds CORS headers to response."""
        origin = request.headers.get("origin")

        # Check if origin is allowed
        if self._is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            logger.debug(f"CORS: Added headers for allowed origin: {origin}")
        # If origin is not allowed, use the first allowed origin
        elif environment.cors_allow_origins:
            response.headers["Access-Control-Allow-Origin"] = (
                environment.cors_allow_origins[0]
            )
            logger.debug(
                f"CORS: Using fallback origin: {environment.cors_allow_origins[0]}"
            )

        # Add other CORS headers
        if environment.cors_allow_credentials:
            response.headers["Access-Control-Allow-Credentials"] = "true"

        if environment.cors_allow_methods:
            response.headers["Access-Control-Allow-Methods"] = ", ".join(
                environment.cors_allow_methods
            )

        if environment.cors_allow_headers:
            response.headers["Access-Control-Allow-Headers"] = ", ".join(
                environment.cors_allow_headers
            )

        return response

    def _is_origin_allowed(self, origin: str | None) -> bool:
        """Checks if origin is allowed."""
        if not origin:
            return False

        # If all origins are allowed
        if "*" in environment.cors_allow_origins:
            return True

        # Check exact match
        if origin in environment.cors_allow_origins:
            return True

        # Check wildcard patterns (e.g., *.example.com)
        for allowed_origin in environment.cors_allow_origins:
            if allowed_origin.startswith("*."):
                domain = allowed_origin[2:]  # Remove "*."
                if origin.endswith(domain):
                    return True

        return False
