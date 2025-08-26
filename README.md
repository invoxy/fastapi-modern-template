# FastAPI Modern Template

Минимальный шаблон современного FastAPI-приложения.

## Стэк

- FastAPI, Uvicorn
- Tortoise ORM
- Loguru (логирование)
- JWT (аутентификация)
- MinIO (файловое хранилище)
- CORS

## Реализовано

- Автообнаружение и регистрация роутеров из `src/apps/`
- Автообнаружение и регистрация роутеров из `src/apps/`, файлы должны называться `routes.py`
- Lifespan инициализация/закрытие ресурсов
- База данных на Tortoise ORM (автогенерация схем)
- JWT-аутентификация
- Интеграция с MinIO
- Middleware для ошибок и аутентификации
- Health check эндпоинт `/health`
- Структурированное логирование

## Установка и запуск

```bash
uv sync
cp env.example .env
uv run python src/main.py
```

## Документация API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health
