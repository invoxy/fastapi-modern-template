import time
import tomllib
from pathlib import Path

from fastapi import APIRouter

from core import database
from core.database.utils import check_database_connection
from core.s3.utils import check_s3_connection
from settings import environment


def get_version() -> str:
    """Gets version from pyproject.toml"""
    try:
        pyproject_path = Path(__file__).parent.parent.parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            return data["project"]["version"]
    except Exception:
        return "unknown"


router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    """Health check endpoint for application status"""
    start_time = time.time()

    # Check database connection
    db_success, db_error = await check_database_connection(environment.database_url)

    # Check S3/MinIO connection
    s3_success, s3_error = await check_s3_connection(
        endpoint_url=environment.minio_public_url,
        aws_access_key_id=environment.minio_access_key,
        aws_secret_access_key=environment.minio_secret_key,
        bucket_name=environment.minio_bucket_name,
        region_name=environment.minio_region,
        is_https=environment.minio_use_https,
    )

    response_time = round((time.time() - start_time) * 1000, 2)  # in milliseconds

    # Determine overall status
    overall_status = "healthy" if db_success and s3_success else "unhealthy"

    return {
        "status": overall_status,
        "timestamp": time.time(),
        "response_time_ms": response_time,
        "api": "ok",
        "database": {
            "status": "ok" if db_success else "error",
            "error": db_error if not db_success else None,
        },
        "s3": {
            "status": "ok" if s3_success else "error",
            "error": s3_error if not s3_success else None,
        },
        "version": get_version(),
    }


@router.get("/health/simple")
async def health_simple():
    """Simple health check without external service verification"""
    return {
        "status": "ok",
        "timestamp": time.time(),
        "api": "running",
        "version": get_version(),
    }
