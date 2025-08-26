from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as exc:
            logger.error("HTTPException: {}", exc)
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        except Exception as e:  # noqa: BLE001
            logger.exception(
                "Internal server error: {}: {}",
                type(e).__name__,
                str(e),
                exc_info=True,
            )
            return JSONResponse(
                status_code=500,
                content={"status": "error", "detail": f"{type(e).__name__}: {e!s}"},
            )
