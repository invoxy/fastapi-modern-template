from core.database.utils import find_tortoise_models
from settings import APPS_PATH, environment

models = find_tortoise_models(APPS_PATH)

TORTOISE_ORM = {
    "connections": {"default": environment.database_url},
    "apps": {
        "models": {
            "models": [*models, "aerich.models"],
            "default_connection": "default",
        }
    },
}
