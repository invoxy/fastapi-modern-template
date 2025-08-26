from loguru import logger
from tortoise.exceptions import IntegrityError

from core.security.password import Password
from settings import environment

from .models import User


async def init_admin():
    try:
        password = Password.hash_password("admin", environment.secret_key)
        await User.create(username="admin", password=password)
    except IntegrityError:
        logger.warning("⚠️  Admin user already exists")
    finally:
        username, password = "admin", "admin"
        logger.warning(f"Username: {username}")
        logger.warning(f"Password: {password}")
