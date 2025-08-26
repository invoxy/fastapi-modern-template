# Autodiscover models and routers

import importlib
import inspect
import os
import sys
from pathlib import Path

from fastapi import FastAPI

from settings import APPS_PATH


def fastapi_routers(root_dir: str | Path, target_filename: str = "routes.py") -> list:
    """Discover FastAPI routers with automatic tag assignment"""
    from fastapi import APIRouter

    root_path = Path(root_dir).resolve()
    routers_data = []

    # Add project root to sys.path for correct imports
    root_parent = root_path.parent
    if str(root_parent) not in sys.path:
        sys.path.insert(0, str(root_parent))

    for file_path in root_path.rglob(target_filename):
        if file_path.is_file():
            try:
                # Build proper module name
                relative_path = file_path.relative_to(root_path)
                module_name = (
                    f"apps.{str(relative_path.with_suffix('')).replace(os.sep, '.')}"
                )

                # Get app directory name for the tag
                app_directory = (
                    relative_path.parts[0] if relative_path.parts else "unknown"
                )
                # Create a hierarchical tag for grouping
                # Use ":" as a hierarchy separator
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

                # Import the module using standard importlib
                module = importlib.import_module(module_name)

                # Look for APIRouter instances in the module
                for attr_name, attr_value in inspect.getmembers(module):
                    if isinstance(attr_value, APIRouter):
                        # Collect router with tag information
                        routers_data.append(
                            {
                                "router": attr_value,
                                "tag": tag_name,
                                "name": attr_name,
                                "module": module_name,
                            }
                        )

            except Exception as e:  # noqa: BLE001
                continue

    return routers_data


def register_routers(app: FastAPI) -> None:
    """Auto-discover and register all routers"""

    routers_data = fastapi_routers(APPS_PATH)

    for router_info in routers_data:
        router = router_info["router"]
        tag = router_info["tag"]
        name = router_info["name"]
        module = router_info["module"]

        # Add router to app
        app.include_router(router)
