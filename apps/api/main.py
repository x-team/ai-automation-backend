from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles

from apps.api.lifespan import lifespan_setup
from apps.api.router import api_router
from apps.core.config import settings
from apps.core.middlewares.ava_server_middleware import AvaServerMiddleware
from apps.core.middlewares.quinn_server_middleware import QuinnServerMiddleware
from apps.core.utils.logger import configure_logging

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="apps",
        version=metadata.version("apps"),
        lifespan=lifespan_setup,
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # TODO: change origins to the frontend URL for production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Quinn server middleware
    app.add_middleware(QuinnServerMiddleware)

    # Ava server middleware
    app.add_middleware(AvaServerMiddleware)

    if settings.storage_provider == "disk":
        # Static files for disk storage
        storage_path = Path(settings.disk_storage_path)
        storage_path.mkdir(parents=True, exist_ok=True)
        app.mount("/static", StaticFiles(directory=str(storage_path)), name="static")

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
