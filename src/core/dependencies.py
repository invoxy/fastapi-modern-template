from apps.users.dependencies import get_current_user
from settings import environment

from .s3 import make_minio_client
from .s3.minio import MinioClient
from .security import make_jwt_manager
from .security.jwt import JWTManager


def get_minio_client() -> MinioClient:
    return make_minio_client(environment)


def get_jwt_manager() -> JWTManager:
    return make_jwt_manager(environment)


__all__ = ["get_current_user", "get_jwt_manager", "get_minio_client"]
