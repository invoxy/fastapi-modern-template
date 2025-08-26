from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = Path(__file__).parent.parent.resolve()
SRC_PATH = ROOT_PATH / "src/"
APPS_PATH = SRC_PATH / "apps/"
CORE_PATH = SRC_PATH / "core/"


class Environment(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_PATH / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database settings
    database_url: str

    # CORS settings
    cors_allow_origins: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_headers: list[str] = Field(default_factory=lambda: ["*"])

    # MinIO settings
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str
    minio_public_url: str
    minio_use_https: bool
    minio_region: str

    # Security settings
    secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int


environment = Environment()
