import sys

from colorama import Fore, Style
from loguru import logger


# Кастомный формат логов
def custom_log_format(record):
    # Цвет для уровня лога
    level_color = {
        "DEBUG": "<blue>{level}</blue>:    ",
        "INFO": "<green>{level}</green>:     ",
        "WARNING": "<yellow>{level}</yellow>:  ",
        "ERROR": "<red>{level}</red>:    ",
        "CRITICAL": "<RED><bold>{level}</bold></RED>: ",
    }.get(record["level"].name, "<white>{level}</white>")  # По умолчанию белый

    return (
        f"{level_color}"  # Уровень лога с цветом
        "{message} "
        "<cyan>({time:YYYY-MM-DD HH:mm:ss})</cyan> "
        "<magenta>[{module}.{function}:{line}]</magenta>\n"
    )


# Настройка логгера
def setup_logger(log_level="INFO"):
    """Настройка логгера с возможностью изменения уровня"""
    logger.remove()  # Удаляем стандартный обработчик
    logger.add(
        sys.stdout,
        format=custom_log_format,
        colorize=True,  # Включаем цвета
        level=log_level,  # Устанавливаем минимальный уровень логов
    )
    return logger


def print_section(title, char="=", length=50, color=Fore.WHITE):
    """
    Печатает разделитель с заголовком по центру в указанном цвете.

    :param title: Текст заголовка
    :param char: Символ для разделителя
    :param length: Общая длина строки
    :param color: Цвет из Fore (например, Fore.RED)
    """
    if len(title) + 4 > length:
        title = title[: length - 7] + "..."  # Обрезаем, если длинный

    line = char * length
    centered_title = title.center(length)

    print(color + line)
    print(centered_title)
    print(line + Style.RESET_ALL)


def print_init_status(success, message, error_details=None):
    """
    Выводит статус инициализации с эмодзи и цветом.

    :param success: bool - успешна ли инициализация
    :param message: str - основное сообщение
    :param error_details: str (необязательно) - детали ошибки (выводятся, если success=False)
    """
    if success:
        print(f"✅ {message}")
    else:
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")
        if error_details:
            print(f"{Fore.RED}  Ошибка: {error_details}{Style.RESET_ALL}")

import functools
import time
from typing import Any, Callable, Optional
from loguru import logger


def log_before(message: Optional[str] = None):
    """
    Decorator to log a message before function execution.

    Args:
        message (Optional[str]): Custom message to log. If None, uses function name.

    Example:
        @log_before("Starting user authentication")
        def authenticate_user(username: str):
            return True

        @log_before()  # Will use function name
        def process_data():
            return "processed"
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Use custom message or function name
            log_message = message or f"Starting {func.__name__}"

            # Log function call with parameters
            if args or kwargs:
                params = []
                if args:
                    params.append(f"args={args}")
                if kwargs:
                    params.append(f"kwargs={kwargs}")
                logger.info(f"🔍 {log_message} | {', '.join(params)}")
            else:
                logger.info(f"🔍 {log_message}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_after(message: str):
    """
    Decorator to log a message after function execution.

    Args:
        message (str): Message to log after function execution.

    Example:
        @log_after("User authentication completed")
        def authenticate_user(username: str):
            return True

        @log_after("Data processing finished")
        def process_data():
            return "processed"
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)

            # Log completion message
            logger.info(f"✅ {message}")

            return result

        return wrapper

    return decorator


def log_execution_time(message: Optional[str] = None):
    """
    Decorator to log function execution time.

    Args:
        message (Optional[str]): Custom message prefix. If None, uses function name.

    Example:
        @log_execution_time("Database query")
        def fetch_users():
            time.sleep(1)
            return []

        @log_execution_time()  # Will use function name
        def slow_operation():
            time.sleep(2)
            return "done"
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            # Use custom message or function name
            log_message = message or func.__name__
            logger.info(f"⏱️ Starting {log_message}")

            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"✅ {log_message} completed in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    f"❌ {log_message} failed after {execution_time:.3f}s: {str(e)}"
                )
                raise

        return wrapper

    return decorator


def log_function_call():
    """
    Decorator to log function calls with parameters and return value.

    Example:
        @log_function_call()
        def add_numbers(a: int, b: int) -> int:
            return a + b
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Log function call
            func_name = func.__name__
            params = []
            if args:
                params.append(f"args={args}")
            if kwargs:
                params.append(f"kwargs={kwargs}")

            param_str = ", ".join(params) if params else "no parameters"
            logger.debug(f"🔍 Calling {func_name}({param_str})")

            try:
                result = func(*args, **kwargs)
                logger.debug(f"✅ {func_name} returned: {result}")
                return result
            except Exception as e:
                logger.error(f"❌ {func_name} raised exception: {str(e)}")
                raise

        return wrapper

    return decorator


def log_async_before(message: Optional[str] = None):
    """
    Async decorator to log a message before async function execution.

    Args:
        message (Optional[str]): Custom message to log. If None, uses function name.

    Example:
        @log_async_before("Starting async database operation")
        async def fetch_data():
            return await db.query()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Use custom message or function name
            log_message = message or f"Starting {func.__name__}"

            # Log function call with parameters
            if args or kwargs:
                params = []
                if args:
                    params.append(f"args={args}")
                if kwargs:
                    params.append(f"kwargs={kwargs}")
                logger.info(f"🔍 {log_message} | {', '.join(params)}")
            else:
                logger.info(f"🔍 {log_message}")

            return await func(*args, **kwargs)

        return wrapper

    return decorator


def log_async_after(message: str):
    """
    Async decorator to log a message after async function execution.

    Args:
        message (str): Message to log after function execution.

    Example:
        @log_async_after("Async database operation completed")
        async def fetch_data():
            return await db.query()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            result = await func(*args, **kwargs)

            # Log completion message
            logger.info(f"✅ {message}")

            return result

        return wrapper

    return decorator


def log_async_execution_time(message: Optional[str] = None):
    """
    Async decorator to log async function execution time.

    Args:
        message (Optional[str]): Custom message prefix. If None, uses function name.

    Example:
        @log_async_execution_time("Async database query")
        async def fetch_users():
            await asyncio.sleep(1)
            return []
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            # Use custom message or function name
            log_message = message or func.__name__
            logger.info(f"⏱️ Starting {log_message}")

            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"✅ {log_message} completed in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    f"❌ {log_message} failed after {execution_time:.3f}s: {str(e)}"
                )
                raise

        return wrapper

    return decorator
