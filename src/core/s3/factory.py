from pydantic_settings import BaseSettings

from .minio import MinioClient


def make_minio_client(settings: object | BaseSettings):
    return MinioClient(
        endpoint_url=settings.minio_public_url,
        aws_access_key_id=settings.minio_access_key,
        bucket_name=settings.minio_bucket_name,
        region_name=settings.minio_region,
        aws_secret_access_key=settings.minio_secret_key,
        is_https=settings.minio_use_https,
    )
