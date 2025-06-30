from typing import Awaitable, Callable

from fastapi import HTTPException, Request, Response
from fastapi import logger as fastapi_logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from apps.core.config import settings

logger = fastapi_logger.logger


class QuinnServerMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate Quinn API key in request headers.

    This middleware checks for an 'X-Quinn-API-Key' header in incoming requests
    and validates it against the configured Quinn API key. If the Quinn API key is
    missing or invalid, it returns a 401 or 403 error respectively.
    """

    def __init__(
        self,
        app: ASGIApp,
        restricted_paths: list[str] | None = None,
    ) -> None:
        """
        Initialize the Quinn API key middleware.

        Args:
            app: The ASGI application
        """
        super().__init__(app)
        self.restricted_paths = restricted_paths or [
            "/api/v1/quinn/generate-slides",
        ]

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        Process the request and validate Quinn API key.

        Args:
            request: The incoming request
            call_next: The next middleware/endpoint to call

        Returns:
            Response: The response from the next middleware/endpoint

        Raises:
            HTTPException: If Quinn API key is missing or invalid
        """
        logger.debug(f"Request to {request.url.path} - Method: {request.method}")

        if request.url.path not in (self.restricted_paths or []):
            logger.debug(
                f"Path {request.url.path} not in restricted paths: {self.restricted_paths}",
            )
            return await call_next(request)

        logger.info(f"Protecting path {request.url.path} - checking API key")
        if not settings.quinn_api_key or settings.quinn_api_key.strip() == "":
            logger.error("No Quinn API key configured in environment variables")
            raise HTTPException(
                status_code=500,
                detail="Server configuration error: Quinn API key not configured. Please contact admin",
            )

        quinn_api_key = request.headers.get("X-Quinn-API-Key")
        if not quinn_api_key:
            logger.warning(f"Quinn API key missing for request to {request.url.path}")
            raise HTTPException(
                status_code=401,
                detail="Quinn API key required. Please include 'X-Quinn-API-Key' header.",
            )

        if quinn_api_key.strip() != settings.quinn_api_key.strip():
            logger.warning(
                f"Invalid Quinn API key provided for request to {request.url.path}",
            )
            raise HTTPException(
                status_code=403,
                detail="Invalid Quinn API key provided.",
            )

        logger.debug(f"Valid Quinn API key provided for request to {request.url.path}")
        return await call_next(request)
