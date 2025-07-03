from typing import Any

from fastapi import HTTPException
from fastapi import logger as fastapi_logger

from apps.core.config import settings

logger = fastapi_logger.logger


class UpdateGoogleDriveFileService:
    """Update Google Drive File Service."""

    def __init__(self) -> None:
        pass

    async def execute(
        self,
        file_id: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """Update Google Drive file."""

        google_drive_service = settings.google_drive_service

        try:
            return (
                google_drive_service.files()
                .update(
                    fileId=file_id,
                    body=body,
                )
                .execute()
            )
        except Exception as err:
            logger.error(err)
            raise HTTPException(
                status_code=404,
                detail="Update Google Drive - file not found",
            ) from err
