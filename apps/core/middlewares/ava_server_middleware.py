from typing import Awaitable, Callable

from fastapi import HTTPException, Request, Response
from fastapi import logger as fastapi_logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from apps.core.config import settings

logger = fastapi_logger.logger


class AvaServerMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate Ava API key in request headers.

    This middleware checks for an 'X-Ava-API-Key' header in incoming requests
    and validates it against the configured Ava API key. If the Ava API key is
    missing or invalid, it returns a 401 or 403 error respectively.
    """

    def __init__(
        self,
        app: ASGIApp,
        restricted_paths: list[str] | None = None,
    ) -> None:
        """
        Initialize the Ava API key middleware.

        Args:
            app: The ASGI application
        """
        super().__init__(app)
        self.restricted_paths = restricted_paths or [
            "/api/v1/ava/messages",
        ]

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        Process the request and validate Ava API key.

        Args:
            request: The incoming request
            call_next: The next middleware/endpoint to call

        Returns:
            Response: The response from the next middleware/endpoint

        Raises:
            HTTPException: If Ava API key is missing or invalid
        """
        logger.debug(f"Request to {request.url.path} - Method: {request.method}")

        if request.url.path not in (self.restricted_paths or []):
            logger.debug(
                f"Path {request.url.path} not in restricted paths: {self.restricted_paths}",
            )
            return await call_next(request)

        logger.info(f"Protecting path {request.url.path} - checking API key")
        if not settings.ava_api_key or settings.ava_api_key.strip() == "":
            logger.error("No Ava API key configured in environment variables")
            raise HTTPException(
                status_code=500,
                detail="Server configuration error: Ava API key not configured. Please contact admin",
            )

        ava_api_key = request.headers.get("X-Ava-API-Key")
        if not ava_api_key:
            logger.warning(f"Ava API key missing for request to {request.url.path}")
            raise HTTPException(
                status_code=401,
                detail="Ava API key required. Please include 'X-Ava-API-Key' header.",
            )

        if ava_api_key.strip() != settings.ava_api_key.strip():
            logger.warning(
                f"Invalid Ava API key provided for request to {request.url.path}",
            )
            raise HTTPException(
                status_code=403,
                detail="Invalid Ava API key provided.",
            )

        logger.debug(f"Valid Ava API key provided for request to {request.url.path}")
        return await call_next(request)
