from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from tortoise import Tortoise

from core.database import find_tortoise_models, init_db
from core.dependencies import get_jwt_manager, get_minio_client
from core.logs import setup_logger
from core.middlewares.auth_error import AuthenticationErrorMiddleware
from core.middlewares.http_error import ErrorHandlingMiddleware
from core.router import register_routers
from core.swagger import setup_custom_swagger_ui
from settings import environment


async def setup_database() -> dict:
    """Initialize database configuration and connection"""
    logger.info("📊 Initializing database...")
    models = find_tortoise_models(Path(__file__).parent / "apps")
    db_config = {
        "connections": {"default": environment.database_url},
        "apps": {
            "models": {
                "models": models,
                "default_connection": "default",
            }
        },
    }
    await init_db(db_config, generate_schemas=True)
    logger.info("✅ Database initialized successfully")
    return db_config


async def setup_services(app: FastAPI) -> None:
    """Initialize and configure application services"""
    logger.info("🔧 Initializing services...")

    # Initialize JWT manager
    jwt_manager = get_jwt_manager()

    # Initialize MinIO client
    minio_client = get_minio_client()

    # Store services in app state for dependency injection
    app.state.jwt_manager = jwt_manager
    app.state.minio_client = minio_client

    logger.info("✅ Services initialized successfully")


async def start_background_tasks() -> None:
    """Start background tasks and services"""
    logger.info("🔄 Starting background tasks...")
    # Здесь можно добавить запуск фоновых задач
    # Например: asyncio.create_task(periodic_task())
    logger.info("✅ Background tasks started")


async def stop_background_tasks() -> None:
    """Stop background tasks and cleanup"""
    logger.info("🛑 Stopping background tasks...")
    # Здесь можно добавить остановку фоновых задач
    logger.info("✅ Background tasks stopped")


async def cleanup_database() -> None:
    """Close database connections"""
    logger.info("🛑 Closing database connections...")
    await Tortoise.close_connections()
    logger.info("✅ Database connections closed")


def setup_middlewares(app: FastAPI) -> None:
    """Configure application middlewares"""
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=environment.cors_allow_origins,
        allow_credentials=environment.cors_allow_credentials,
        allow_methods=environment.cors_allow_methods,
        allow_headers=environment.cors_allow_headers,
    )

    # Add custom middlewares
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(AuthenticationErrorMiddleware)


def create_fastapi_app() -> FastAPI:
    """Create and configure FastAPI application instance"""
    return FastAPI(
        lifespan=lifespan,
        docs_url=None,  # Отключаем стандартный Swagger UI
        redoc_url=None,  # Отключаем ReDoc
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting FastAPI application...")

    # Register routers
    register_routers(app)

    # Initialize database
    await setup_database()

    # Initialize services
    await setup_services(app)

    # Start background tasks
    await start_background_tasks()

    logger.info("🎉 Application startup completed!")
    await setup_custom_swagger_ui(app)

    yield

    # Shutdown
    logger.info("🛑 Shutting down application...")

    # Stop background tasks
    await stop_background_tasks()

    # Cleanup database
    await cleanup_database()

    logger.info("👋 Application shutdown completed!")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    # Setup logging first
    setup_logger()

    # Create FastAPI app with lifespan
    app = create_fastapi_app()

    # Setup middlewares
    setup_middlewares(app)

    return app


# Create application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
