from typing import Any

from fastapi import HTTPException
from fastapi import logger as fastapi_logger

from apps.core.config import settings

logger = fastapi_logger.logger


class ShowGoogleSlidesFileService:
    """Show Google Slides File Service."""

    def __init__(self) -> None:
        """Initialize the Show Google Slides File Service."""

    async def execute(
        self,
        presentation_id: str,
    ) -> dict[str, Any]:
        """Execute the Show Google Slides File Service."""

        google_slides_service = settings.google_slides_service

        try:
            return (
                google_slides_service.presentations()
                .get(
                    presentationId=presentation_id,
                )
                .execute()
            )
        except Exception as err:
            logger.error(err)
            raise HTTPException(
                status_code=404,
                detail="Show Google Slides - file not found",
            ) from err
