# FastAPI Modern Template

Современный шаблон FastAPI с удобными функциями для быстрой разработки веб-приложений.

## 🚀 Возможности

- **Удобная регистрация роутеров** - автоматическая регистрация из структуры приложений
- **Фабрика приложений** - простой способ создания и настройки FastAPI приложений
- **Менеджеры компонентов** - для middleware, событий и других компонентов
- **Структурированная архитектура** - четкое разделение на модули и приложения
- **Автоматическая инициализация** - базы данных, логирования, фоновых задач
- **Готовые компоненты** - CORS, обработчики исключений, проверка здоровья

## 📁 Структура проекта

```
src/
├── apps/                    # Приложения
│   └── example/            # Пример приложения
│       ├── __init__.py
│       └── routes.py       # Роутеры приложения
├── core/                   # Основные компоненты
│   ├── app.py             # Классы приложений
│   ├── initializers/      # Инициализаторы
│   │   ├── app_factory.py # Фабрика приложений
│   │   ├── events.py      # Управление событиями
│   │   ├── router_registry.py # Регистрация роутеров
│   │   ├── middleware.py  # Управление middleware
│   │   └── tasks.py       # Фоновые задачи
│   └── ...
├── main.py                # Основной файл приложения
└── settings.py           # Настройки
```

## 🛠️ Способы создания приложения

### 1. Фабрика приложений (рекомендуется)

```python
from core.initializers import create_app_factory

# Создаем фабрику
factory = create_app_factory(
    title="Мое приложение",
    description="Описание приложения",
    version="1.0.0",
    debug=True
)

# Настраиваем приложение
factory.create_app()
factory.add_health_check()
factory.add_default_exception_handlers()
factory.add_cors(allow_origins=["*"])

# Добавляем функции запуска/завершения
factory.add_startup_function(setup_database)
factory.add_shutdown_function(cleanup_resources)

# Настраиваем lifespan
factory.setup_lifespan()

# Получаем приложение
app = factory.build()
```

### 2. Стандартное приложение

```python
from core.initializers import create_standard_app

app = create_standard_app(
    title="Стандартное приложение",
    cors_origins=["*"],
    add_health_check=True,
    add_exception_handlers=True
)
```

### 3. Ручное создание

```python
from core.app import FastAPIApp
from core.initializers import register_routers_from_apps

app = FastAPIApp(
    title="Ручное приложение",
    description="Описание",
    version="1.0.0"
)

# Регистрируем роутеры
register_routers_from_apps(
    app.get_app(),
    apps_dir="src/apps",
    prefix_pattern="/api/{app_name}"
)
```

## 📦 Регистрация роутеров

### Автоматическая регистрация из приложений

```python
from core.initializers import register_routers_from_apps

register_routers_from_apps(
    app,
    apps_dir="src/apps",
    prefix_pattern="/api/{app_name}",  # /api/users, /api/auth
    tags_pattern="{app_name}"          # users, auth
)
```

Структура приложения:
```
apps/
├── users/
│   └── routes.py  # router = APIRouter()
├── auth/
│   └── routes.py  # router = APIRouter()
└── api/
    └── routes.py  # router = APIRouter()
```

### Ручная регистрация с конфигурацией

```python
from core.initializers import register_router_with_config

config = {
    "prefix": "/api/v1",
    "tags": ["api"],
    "dependencies": [auth_dependency],
    "responses": {404: {"description": "Not found"}}
}

register_router_with_config(app, router, config)
```

## 🔧 Middleware

### Менеджер middleware

```python
from core.initializers import create_middleware_manager

manager = create_middleware_manager(app)

manager.add_cors(
    allow_origins=["*"],
    allow_credentials=True
)

manager.add_trusted_host(["localhost", "127.0.0.1"])

manager.add_custom(MyCustomMiddleware, option="value")
```

### Кастомный middleware

```python
from core.initializers import CustomMiddleware

class LoggingMiddleware(CustomMiddleware):
    async def dispatch(self, request, call_next):
        print(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        print(f"Response: {response.status_code}")
        return response
```

## 📅 События

### Менеджер событий

```python
from core.initializers import create_event_manager

manager = create_event_manager(app)

manager.add_startup_event(setup_database, "database_setup")
manager.add_shutdown_event(cleanup_resources, "cleanup")
manager.add_exception_handler(ValueError, handle_value_error)
```

### Готовые функции

```python
from core.initializers import (
    register_default_exception_handlers,
    register_health_check_event,
    register_database_events
)

register_default_exception_handlers(app)
register_health_check_event(app)
register_database_events(app, startup_db_func, shutdown_db_func)
```

## 🎯 Примеры использования

### Простое приложение

```python
# main.py
from core.initializers import create_standard_app
from core.initializers import register_routers_from_apps
from settings import APPS_PATH

app = create_standard_app(
    title="Мое API",
    cors_origins=["*"]
)

register_routers_from_apps(app, APPS_PATH)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Сложное приложение

```python
# main.py
from core.initializers import create_app_factory
from core.initializers import register_routers_from_apps
from settings import APPS_PATH

async def setup_database():
    # Инициализация БД
    pass

async def cleanup_resources():
    # Очистка ресурсов
    pass

# Создаем фабрику
factory = create_app_factory(
    title="Сложное приложение",
    description="API с множеством функций",
    version="2.0.0"
)

# Настраиваем приложение
factory.create_app()
factory.add_health_check()
factory.add_default_exception_handlers()
factory.add_cors(allow_origins=["https://myapp.com"])
factory.add_startup_function(setup_database)
factory.add_shutdown_function(cleanup_resources)
factory.setup_lifespan()

# Получаем приложение
app = factory.build()

# Регистрируем роутеры
register_routers_from_apps(
    app,
    apps_dir=APPS_PATH,
    prefix_pattern="/api/v2/{app_name}"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🔄 Фоновые задачи

```python
# tasks.py
async def register():
    """Регистрирует фоновые задачи."""
    # Ваш код инициализации задач
    pass
```

## 📝 Создание нового приложения

1. Создайте папку в `src/apps/`:
```bash
mkdir src/apps/myapp
```

2. Создайте `routes.py`:
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def hello():
    return {"message": "Hello from myapp"}
```

3. Роутер автоматически зарегистрируется с префиксом `/api/myapp`

## 🚀 Запуск

```bash
python src/main.py
```

## 📚 Дополнительные возможности

- **Автоматическая документация** - Swagger UI на `/docs`
- **Логирование** - Настроенный Loguru
- **База данных** - Tortoise ORM с автоматической инициализацией
- **Безопасность** - JWT, пароли, CORS
- **Файловое хранилище** - MinIO интеграция
- **Фоновые задачи** - Автоматическая регистрация

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License 
