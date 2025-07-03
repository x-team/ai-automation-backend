from fastapi import HTTPException
from fastapi import logger as fastapi_logger

from apps.core.config import settings

logger = fastapi_logger.logger


class ShowGoogleDriveFileService:
    """Show Google Drive File Service."""

    def __init__(self) -> None:
        """Initialize the Show Google Drive File Service."""

    async def execute(
        self,
        file_id: str,
    ) -> dict[str, str]:
        """Execute the Show Google Drive File Service."""

        google_drive_service = settings.google_drive_service

        try:
            return (
                google_drive_service.files()
                .get(
                    fileId=file_id,
                    supportsAllDrives=True,
                )
                .execute()
            )
        except Exception as err:
            logger.error(err)
            raise HTTPException(
                status_code=404,
                detail="Show Google Drive - file not found",
            ) from err
