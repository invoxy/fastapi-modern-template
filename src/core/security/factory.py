from pydantic_settings import BaseSettings

from .jwt import JWTManager


def make_jwt_manager(settings: object | BaseSettings) -> JWTManager:
    """
    Factory function to create JWTManager instance from settings.

    :param settings: Application settings containing JWT configuration
    :return: Configured JWTManager instance
    """
    return JWTManager(
        algorithm=settings.jwt_algorithm,
        expiration_minutes=settings.jwt_expire_minutes,
        secret_key=settings.secret_key,
    )
