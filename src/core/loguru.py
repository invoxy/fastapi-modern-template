import sys

from colorama import Fore, Style
from loguru import logger

# Remove default handler
logger.remove()

# Define maximum level length for alignment
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
MAX_LEVEL_LENGTH = max(len(level) for level in LOG_LEVELS)


# Custom log format
def custom_log_format(record):
    # Color for log level
    level_colors = {
        "DEBUG": "<blue>{level}</blue>",
        "INFO": "<green>{level}</green>",
        "WARNING": "<yellow>{level}</yellow>",
        "ERROR": "<red>{level}</red>",
        "CRITICAL": "<RED><bold>{level}</bold></RED>",
    }

    # Get colored level
    level_name = record["level"].name
    colored_level = level_colors.get(level_name, "<white>{level}</white>")

    # Calculate padding spaces for alignment
    padding_length = MAX_LEVEL_LENGTH - len(level_name)
    padding = " " * padding_length

    return (
        f"{colored_level}{padding}: "  # Log level with color and alignment
        "{message} "
        "<cyan>({time:YYYY-MM-DD HH:mm:ss})</cyan> "
        "<magenta>[{module}.{function}:{line}]</magenta>\n"
    )


# Logger setup
def setup_logger():
    """Configure logging with custom format."""
    # Add console handler
    logger.add(
        sys.stdout,
        format=custom_log_format,
        level="DEBUG",
        colorize=True,
    )


def print_section(title: str, color: str = "blue"):
    """Print section header."""

    color_map = {
        "blue": Fore.BLUE,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "red": Fore.RED,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
    }

    selected_color = color_map.get(color, Fore.BLUE)
    print(f"\n{selected_color}{'=' * 50}")  # noqa: T201
    print(f"{title:^50}")  # noqa: T201
    print(f"{'=' * 50}{Style.RESET_ALL}\n")  # noqa: T201


def print_init_status(success: bool, message: str, error_details=None):  # noqa: FBT001
    if success:
        status = f"{Fore.GREEN}✓{Style.RESET_ALL}"
        print(f"{status} {message}")  # noqa: T201
    else:
        status = f"{Fore.RED}✗{Style.RESET_ALL}"
        print(f"{status} {message}")  # noqa: T201
        if error_details:
            print(f"   {Fore.YELLOW}Details: {error_details}{Style.RESET_ALL}")  # noqa: T201
