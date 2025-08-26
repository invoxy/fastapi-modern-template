from fastapi_utils.tasks import repeat_every
from loguru import logger


@repeat_every(seconds=10)
async def check_status():
    logger.info("Test task << 10 seconds >>")
