# FastAPI Modern Template

Minimal template for a modern FastAPI application.

## Stack

- FastAPI, Uvicorn
- Tortoise ORM
- Loguru (logging)
- JWT (authentication)
- MinIO (object storage)
- CORS

## Implemented

- Auto-discovery and registration of routers from `src/apps/` (files must be named `routes.py`)
- Lifespan initialization/shutdown of resources
- Database via Tortoise ORM (schema generation)
- JWT authentication
- MinIO integration
- Middleware for errors and authentication
- Health check endpoint `/health`
- Structured logging

## Install and run

```bash
uv sync
cp env.example .env
uv run python src/main.py
```

## API docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health
