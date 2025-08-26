from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from tortoise import Tortoise

from core.database import init_db
from core.database.utils import check_database_connection
from core.logs import setup_logger
from core.middlewares.auth_error import AuthenticationErrorMiddleware
from core.middlewares.cors import CORSMiddleware
from core.middlewares.http_error import ErrorHandlingMiddleware
from core.router import register_routers
from core.swagger import setup_custom_swagger_ui
from database_config import TORTOISE_ORM
from settings import environment


async def setup_database() -> dict:
    """Initialize database configuration and connection"""
    # Check database connection
    success, error = await check_database_connection(environment.database_url)

    if not success:
        logger.error(f"❌ Database connection failed: {error}")
    else:
        logger.info("✅ Database initialized successfully")

    await init_db(TORTOISE_ORM, generate_schemas=True)


def setup_middlewares(app: FastAPI) -> None:
    """Configure application middlewares"""
    # Add custom CORS middleware
    app.add_middleware(CORSMiddleware)
    # Add custom middlewares
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(AuthenticationErrorMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Register routers
    register_routers(app)
    await setup_database()

    await setup_custom_swagger_ui(app)

    yield

    await Tortoise.close_connections()


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    # Setup logging first
    setup_logger()

    # Create FastAPI app with lifespan
    app = FastAPI(
        lifespan=lifespan,
        docs_url=None,  # Disable default Swagger UI
        redoc_url=None,  # Disable ReDoc
    )

    # Setup middlewares
    setup_middlewares(app)

    return app


# Create application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
