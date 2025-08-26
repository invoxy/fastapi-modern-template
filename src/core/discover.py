# Autodiscover models and routers

import importlib
import inspect
import os
import sys
from pathlib import Path

from loguru import logger



def fastapi_routers(root_dir: str | Path, target_filename: str = "routes.py") -> list:
    """Discover FastAPI routers with automatic tag assignment"""
    from fastapi import APIRouter

    root_path = Path(root_dir).resolve()
    routers_data = []

    # Добавляем корневую директорию в sys.path для корректных импортов
    root_parent = root_path.parent
    if str(root_parent) not in sys.path:
        sys.path.insert(0, str(root_parent))

    logger.debug(f"🔍 Searching for routers in directory: {root_path}")

    for file_path in root_path.rglob(target_filename):
        if file_path.is_file():
            try:
                # Создаем правильное имя модуля
                relative_path = file_path.relative_to(root_path)
                module_name = (
                    f"apps.{str(relative_path.with_suffix('')).replace(os.sep, '.')}"
                )

                # Получаем название директории приложения для тега
                app_directory = (
                    relative_path.parts[0] if relative_path.parts else "unknown"
                )
                # Создаем иерархический тег для группировки
                # Используем ":" как разделитель для иерархии
                category_mapping = {
                    "authentication": "Auth:Authentication",
                    "acl": "Auth:Access Control",
                    "folders_manager": "Data:Folders Manager",
                    "group_manager": "Data:Group Manager",
                    "secure_data": "Data:Secure Data",
                    "template_manager": "Data:Template Manager",
                    "static_manager": "Utils:Static Manager",
                }

                tag_name = category_mapping.get(
                    app_directory, f"Apps:{app_directory.replace('_', ' ').title()}"
                )

                # Импортируем модуль стандартным способом
                module = importlib.import_module(module_name)

                # Ищем APIRouter в модуле
                for attr_name, attr_value in inspect.getmembers(module):
                    if isinstance(attr_value, APIRouter):
                        logger.debug(f"✅ Found router: {attr_name} in {module_name}")

                        # Возвращаем роутер с информацией о теге
                        routers_data.append(
                            {
                                "router": attr_value,
                                "tag": tag_name,
                                "name": attr_name,
                                "module": module_name,
                            }
                        )

            except Exception as e:  # noqa: BLE001
                logger.error(f"❌ Error processing file {file_path}: {e}")
                # Continue processing other files
                continue

    logger.debug(f"🎯 Found routers: {len(routers_data)}")
    return routers_data
