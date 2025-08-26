from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from settings import CORE_PATH


async def setup_custom_swagger_ui(app: FastAPI):
    """Setup custom Swagger UI"""

    app.docs_url = None
    app.redoc_url = None

    app.mount(
        "/swagger/",
        StaticFiles(directory=CORE_PATH / "swagger"),
        name="swagger_static",
    )

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        """Custom Swagger UI with hierarchical tags support"""

        # Read custom HTML template

        # Read custom HTML template
        with open(CORE_PATH / "swagger" / "swagger-ui.html") as f:
            html_content = f.read()

        # Replace placeholders

        html_content = html_content.replace("{{title}}", "API Documentation")
        html_content = html_content.replace("{{openapi_url}}", "/openapi.json")

        return HTMLResponse(content=html_content, media_type="text/html")
