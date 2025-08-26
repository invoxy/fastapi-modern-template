import os
from pathlib import Path
from urllib.parse import urlparse

from loguru import logger
from pydantic import BaseModel, field_validator


class DatabaseConfig(BaseModel):
    """
    Configuration model for database connection parameters.

    This class provides a structured way to store and validate database connection
    information including user credentials, host details, and database name.
    It includes validation for all fields to ensure data integrity.

    Attributes:
        user (str): Database username for authentication.
        password (str): Database password for authentication.
        host (str): Database server hostname or IP address.
        port (int): Database server port number (must be less than 4 digits).
        database_name (str): Name of the database to connect to.

    Example:
        config = DatabaseConfig(
            user="myuser",
            password="mypassword",
            host="localhost",
            port=3306,
            database_name="mydb"
        )

        # Or parse from URL
        config = DatabaseConfig.parse_database_url(
            "mysql://user:pass@localhost:3306/database"
        )
    """

    user: str
    password: str
    host: str
    port: int
    database_name: str

    @field_validator("database_name")
    def validate_database_name(cls, v: str) -> str:
        """
        Validates that the database name is not empty.

        Args:
            v (str): The database name to validate.

        Returns:
            str: The validated database name.

        Raises:
            ValueError: If the database name is empty.
        """
        if not v:
            raise ValueError("Database name cannot be empty")
        return v

    @field_validator("port")
    def validate_port(cls, v: int) -> int:
        """
        Validates that the port number is within acceptable range.

        Args:
            v (int): The port number to validate.

        Returns:
            int: The validated port number.

        Raises:
            ValueError: If the port number has more than 4 digits.
        """
        if len(str(v)) > 4:
            raise ValueError("Port must be less than 4 digits")
        return v

    @field_validator("host")
    def validate_host(cls, v: str) -> str:
        """
        Validates that the host is not empty.

        Args:
            v (str): The host to validate.

        Returns:
            str: The validated host.

        Raises:
            ValueError: If the host is empty.
        """
        if not v:
            raise ValueError("Host cannot be empty")
        return v

    @field_validator("user")
    def validate_user(cls, v: str) -> str:
        """
        Validates that the username is not empty.

        Args:
            v (str): The username to validate.

        Returns:
            str: The validated username.

        Raises:
            ValueError: If the username is empty.
        """
        if not v:
            raise ValueError("User cannot be empty")
        return v

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """
        Validates that the password is not empty.

        Args:
            v (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password is empty.
        """
        if not v:
            raise ValueError("Password cannot be empty")
        return v


def parse_database_url(database_url: str) -> DatabaseConfig:
    """
    Parses a MySQL connection string and returns a DatabaseConfig instance.

    This method takes a standard MySQL connection URL and extracts all
    the individual components (user, password, host, port, database name)
    to create a DatabaseConfig object.

    Args:
        database_url (str): MySQL connection string in format:
                            mysql://user:password@host:port/database_name

    Returns:
        DatabaseConfig: A new DatabaseConfig instance with parsed values.

    Example:
        config = DatabaseConfig.parse_database_url(
            "mysql://myuser:mypass@localhost:3306/mydatabase"
        )

    Note:
        The method uses urlparse to safely extract components from the URL.
        All extracted values will be validated by the field validators.
    """
    # Parse connection string
    parsed_url = urlparse(database_url)

    # Extract individual components
    user = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port
    database_name = parsed_url.path.lstrip("/")

    return DatabaseConfig(
        user=user,
        password=password,
        host=host,
        port=port,
        database_name=database_name,
    )


def find_tortoise_models(
    root_dir: str | Path, target_filename: str = "models.py"
) -> list:
    """Discover Tortoise ORM models"""
    models = []

    logger.info(f"🔍 Searching for models in directory: {root_dir}")

    for file_path in root_dir.rglob(target_filename):
        if file_path.is_file():
            relative_path = file_path.relative_to(root_dir)
            module_path = (
                f"apps.{str(relative_path.with_suffix('')).replace(os.sep, '.')}"
            )
            models.append(module_path)

    logger.info(f"🎯 Found models: {len(models)}")
    return models
