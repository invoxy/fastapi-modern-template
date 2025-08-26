# FastAPI Modern Template 🚀

Minimal, production-minded scaffold for building FastAPI services ✨

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009485?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)

## Features ✨

- ✅ Auto-discovery of app routers from `src/apps/*/routes.py`
- ✅ Lifespan hooks for init/shutdown of resources
- ✅ Tortoise ORM with automatic schema generation
- 🔐 JWT auth with pluggable security factory
- 🗃️ MinIO S3-compatible object storage
- 🛡️ Error/auth middlewares + structured logging (Loguru)
- 💓 Health check endpoint at `/health`
- 🎨 Custom Swagger UI (HTML/CSS overrides)

## Tech stack 🧰

- **API** 🔌: FastAPI, Uvicorn
- **ORM** 🗄️: Tortoise ORM
- **Auth** 🔐: JWT
- **Storage** 🗃️: MinIO (S3)
- **Logging** 🧾: Loguru
- **CORS** 🌐: configurable middleware

## Quickstart ⚡

```bash
uv sync
cp env.example .env
uv run python src/main.py
```

App runs on `http://localhost:8000`.

## API docs 📚

- 📘 Swagger UI: `http://localhost:8000/docs`
- 📕 ReDoc: `http://localhost:8000/redoc`
- 💓 Health: `http://localhost:8000/health`

### Custom Swagger UI 🎨

This project ships with a custom Swagger UI template and styles:

- HTML: `src/core/swagger/swagger-ui.html`
- CSS: `src/core/swagger/swagger-ui.css`

Edit these files to tweak look & feel, logo, colors, meta tags, or UI behavior. The customized page is served at `/docs`, replacing FastAPI’s default template.

## Configuration ⚙️

Copy `.env` from the example and adjust values:

```bash
cp env.example .env
```

Common variables in `.env`:

- `APP_ENV`: environment name (e.g., `local`, `prod`)
- `SECRET_KEY`: JWT signing secret
- `DATABASE_URL`: Tortoise DB URL (e.g., `sqlite://db.sqlite3`)
- `S3_ENDPOINT`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET`, `S3_REGION`: MinIO/S3 settings
- `CORS_ORIGINS`: comma-separated origins

See `env.example` for the full list.

## Project layout 🗂️

```text
src/
  apps/
    health/        # /health endpoint
    users/         # user models, routes, deps
  core/
    database/      # DB mixins and utils
    middlewares/   # error/auth/cors
    security/      # jwt/password/factory
    s3/            # minio factory & utils
  main.py          # app factory, startup
```

## Development 🛠️

- ▶️ Run app: `uv run python src/main.py`
- 🧹 Format/lint: configured via `pyproject.toml`

## License 📄

MIT — see `LICENSE`.
