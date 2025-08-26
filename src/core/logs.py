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
