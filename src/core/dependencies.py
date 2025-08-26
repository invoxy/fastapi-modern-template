from settings import environment

from .s3 import make_minio_client
from .s3.minio import MinioClient
from .security import make_jwt_manager
from .security.jwt import JWTManager


def get_minio_client() -> MinioClient:
    return make_minio_client(environment)


def get_jwt_manager() -> JWTManager:
    return make_jwt_manager(environment)
