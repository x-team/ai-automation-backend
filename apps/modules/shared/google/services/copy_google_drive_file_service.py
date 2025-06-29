from typing import Any

from fastapi import HTTPException
from fastapi import logger as fastapi_logger

from apps.core.config import settings

logger = fastapi_logger.logger


class CopyGoogleDriveFileService:
    """Copy Google Drive File Service."""

    def __init__(self) -> None:
        pass

    async def execute(
        self,
        file_id: str,
    ) -> dict[str, Any]:
        """Copy Google Drive file."""

        google_drive_service = settings.google_drive_service

        try:
            return (
                google_drive_service.files()
                .copy(
                    fileId=file_id,
                    supportsAllDrives=True,
                )
                .execute()
            )
        except Exception as err:
            logger.error(err)
            raise HTTPException(status_code=404, detail="File not found") from err
