from tortoise import Tortoise

from .mixins import TimestampMixin
from .utils import find_tortoise_models, parse_database_url


async def init_db(config: dict, *, generate_schemas: bool = True):
    """
    Initialize a single database connection using Tortoise ORM.

    This function sets up the database connection with the provided configuration
    and optionally generates database schemas based on the models.

    Args:
        config (dict): Database configuration dictionary containing connection
                      parameters and model definitions for Tortoise ORM.
        generate_schemas (bool, optional): Whether to generate database schemas
                                         based on the models. Defaults to True.
                                         Set to False if you want to handle schema
                                         generation manually or if schemas already exist.

    Example:
        config = {
            "connections": {
                "default": "mysql://user:pass@localhost:3306/db"
            },
            "apps": {
                "models": {
                    "models": ["app.models"],
                    "default_connection": "default"
                }
            }
        }
        await init_db(config)

    Note:
        This function is asynchronous and must be awaited. It will initialize
        the Tortoise ORM connection pool and optionally create database tables
        based on your model definitions.
    """
    await Tortoise.init(
        config=config,
    )
    if generate_schemas:
        await Tortoise.generate_schemas()


async def init_dbs(*db_configs: tuple):
    """
    Initialize multiple database connections.

    This function allows you to initialize multiple databases simultaneously.
    Each database configuration is a tuple containing the config dict and
    a boolean flag for schema generation.

    Args:
        *db_configs (tuple): Variable number of tuples, where each tuple contains:
                            - config (dict): Database configuration dictionary
                            - generate_schemas (bool): Whether to generate schemas for this database

    Example:
        db1_config = {
            "connections": {"default": "mysql://user:pass@localhost:3306/db1"},
            "apps": {"models": {"models": ["app.models1"], "default_connection": "default"}}
        }
        db2_config = {
            "connections": {"default": "mysql://user:pass@localhost:3306/db2"},
            "apps": {"models": {"models": ["app.models2"], "default_connection": "default"}}
        }

        await init_dbs(
            (db1_config, True),   # Generate schemas for db1
            (db2_config, False)   # Don't generate schemas for db2
        )

    Note:
        This function processes each database configuration sequentially.
        If any database initialization fails, the function will raise an exception
        and stop processing remaining configurations.
    """
    for db_config, generate_schemas in db_configs:
        await init_db(db_config, generate_schemas=generate_schemas)


__all__ = [
    "TimestampMixin",
    "find_tortoise_models",
    "init_db",
    "init_dbs",
    "parse_database_url",
]
