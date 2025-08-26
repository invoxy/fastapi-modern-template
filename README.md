# FastAPI Modern Template

Современный шаблон FastAPI приложения с комплексной архитектурой и автоматической инициализацией.

## 🚀 Особенности

- **Автоматическое обнаружение роутеров** - все роутеры в папке `apps/` автоматически регистрируются
- **Lifespan management** - правильная инициализация и закрытие ресурсов
- **База данных** - Tortoise ORM с автоматической генерацией схем
- **Аутентификация** - JWT токены с настраиваемыми параметрами
- **Файловое хранилище** - интеграция с MinIO
- **CORS** - настраиваемые CORS параметры
- **Логирование** - структурированное логирование с Loguru
- **Фоновые задачи** - поддержка периодических задач
- **Middleware** - обработка ошибок и аутентификации
- **Health check** - эндпоинт для проверки состояния приложения

## 📦 Установка

1. Клонируйте репозиторий:

```bash
git clone <repository-url>
cd fastapi-modern-template
```

2. Установите зависимости:

```bash
uv sync
```

3. Скопируйте файл с переменными окружения:

```bash
cp env.example .env
```

4. Настройте переменные окружения в файле `.env`

## 🔧 Настройка

### Переменные окружения

Создайте файл `.env` на основе `env.example`:

```bash
# База данных
DATABASE_URL=sqlite://./db.sqlite3

# CORS настройки
CORS_ALLOW_ORIGINS=["*"]
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]

# MinIO настройки
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
MINIO_BUCKET_NAME=your_bucket_name
MINIO_PUBLIC_URL=http://localhost:9000
MINIO_USE_HTTPS=false
MINIO_REGION=us-east-1

# Безопасность
SECRET_KEY=your_secret_key_here_make_it_long_and_random
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
SECURITY_ALGORITHM=HS256
```

## 🏃‍♂️ Запуск

### Разработка

```bash
uv run python src/main.py
```

### Продакшн

```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## 📁 Структура проекта

```
src/
├── apps/                    # Приложения
│   └── users/              # Модуль пользователей
│       ├── models.py       # Модели данных
│       ├── routes.py       # API роуты
│       └── dependencies.py # Зависимости
├── core/                   # Ядро приложения
│   ├── database/          # Работа с БД
│   ├── dependencies.py    # Общие зависимости
│   ├── loguru.py         # Настройка логирования
│   ├── middlewares/      # Middleware
│   ├── router.py         # Автообнаружение роутеров
│   ├── s3/               # MinIO интеграция
│   └── security/         # Безопасность
├── main.py               # Точка входа
├── settings.py           # Настройки
└── tasks.py              # Фоновые задачи
```

## 🔌 Добавление новых модулей

1. Создайте папку в `src/apps/` (например, `src/apps/products/`)
2. Создайте файл `routes.py` с APIRouter:

```python
from fastapi import APIRouter

router = APIRouter(tags=["Products"])

@router.get("/products")
async def get_products():
    return {"products": []}
```

3. Роутер автоматически будет обнаружен и зарегистрирован!

## 📊 API документация

После запуска приложения доступна автоматическая документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## 🛠️ Разработка

### Линтинг и форматирование

```bash
uv run ruff check src/
uv run ruff format src/
```

### Тестирование

```bash
# Добавьте тесты в папку tests/
uv run pytest
```

## 📝 Логи

Приложение использует структурированное логирование с Loguru. Логи включают:

- 🚀 Запуск приложения
- 📊 Инициализация базы данных
- 🔧 Инициализация сервисов
- 🔄 Запуск фоновых задач
- 🔍 Обнаружение роутеров
- ✅ Регистрация роутеров
- 🛑 Завершение работы

## 🔒 Безопасность

- JWT токены для аутентификации
- Настраиваемые CORS параметры
- Middleware для обработки ошибок аутентификации
- Безопасное хранение файлов через MinIO

## 🚀 Готово к продакшну

- Lifespan management для правильного управления ресурсами
- Health check эндпоинт
- Структурированное логирование
- Настраиваемые параметры через переменные окружения
- Автоматическая документация API
