from typing import Any

from fastapi import HTTPException
from fastapi import logger as fastapi_logger

from apps.core.config import settings

logger = fastapi_logger.logger


class UpdateGoogleSlidesFileService:
    """Update Google Slides File Service."""

    def __init__(self) -> None:
        """Initialize the Update Google Slides File Service."""

    async def execute(
        self,
        presentation_id: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute the Update Google Slides File Service."""

        google_slides_service = settings.google_slides_service

        try:
            return (
                google_slides_service.presentations()
                .batchUpdate(
                    presentationId=presentation_id,
                    body=body,
                )
                .execute()
            )
        except Exception as err:
            logger.error(err)
            raise HTTPException(
                status_code=404,
                detail="Update Google Slides - file not found",
            ) from err
