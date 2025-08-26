import sys

from colorama import Fore, Style
from loguru import logger


# Custom log format
def custom_log_format(record):
    # Color for log level
    level_color = {
        "DEBUG": "<blue>{level}</blue>:    ",
        "INFO": "<green>{level}</green>:     ",
        "WARNING": "<yellow>{level}</yellow>:  ",
        "ERROR": "<red>{level}</red>:    ",
        "CRITICAL": "<RED><bold>{level}</bold></RED>: ",
    }.get(record["level"].name, "<white>{level}</white>")  # Default white

    return (
        f"{level_color}"  # Level with color
        "{message} "
        "<cyan>({time:YYYY-MM-DD HH:mm:ss})</cyan> "
        "<magenta>[{module}.{function}:{line}]</magenta>\n"
    )


# Logger setup
def setup_logger(log_level="INFO"):
    """Configure logger with adjustable level"""
    logger.remove()  # Remove default handler
    logger.add(
        sys.stdout,
        format=custom_log_format,
        colorize=True,  # Enable colors
        level=log_level,  # Set minimum log level
    )
    return logger


def print_section(title, char="=", length=50, color=Fore.WHITE):
    """
    Print a divider with a centered title in the specified color.

    :param title: Title text
    :param char: Divider character
    :param length: Total line length
    :param color: Color from Fore (e.g., Fore.RED)
    """
    if len(title) + 4 > length:
        title = title[: length - 7] + "..."  # Trim if too long

    line = char * length
    centered_title = title.center(length)

    print(color + line)
    print(centered_title)
    print(line + Style.RESET_ALL)


def print_init_status(success, message, error_details=None):
    """
    Print initialization status with emoji and color.

    :param success: bool - whether initialization succeeded
    :param message: str - main message
    :param error_details: str (optional) - error details (shown if success=False)
    """
    if success:
        print(f"✅ {message}")
    else:
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")
        if error_details:
            print(f"{Fore.RED}  Error: {error_details}{Style.RESET_ALL}")
