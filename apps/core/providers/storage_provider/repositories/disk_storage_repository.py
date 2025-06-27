import base64
import uuid
from pathlib import Path

from fastapi import HTTPException
from fastapi import logger as fastapi_logger

from apps.core.config import settings
from apps.core.providers.storage_provider.repository_interfaces.storage_repository_interface import (
    IStorageProvider,
)

logger = fastapi_logger.logger


class DiskStorageRepository(IStorageProvider):
    """Disk storage repository."""

    def __init__(self) -> None:
        """Initialize disk storage directory."""
        self.storage_path = Path(settings.disk_storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    async def upload_file(self, file_path: str, file_name: str) -> str:
        """Upload a file to the local disk storage.

        Args:
            file_path: Either a file path on disk or base64 encoded file data
            file_name: The name to use for the uploaded file

        Returns:
            The public URL of the uploaded file
        """
        try:
            file_extension = Path(file_name).suffix
            unique_filename = (
                f"{Path(file_name).stem}_{uuid.uuid4().hex[:8]}{file_extension}"
            )
            destination_path = self.storage_path / unique_filename

            if self._is_base64(file_path):
                file_data = base64.b64decode(file_path)
                with destination_path.open("wb") as f:
                    f.write(file_data)
            else:
                source_path = Path(file_path)
                if not source_path.exists():
                    raise HTTPException(
                        status_code=404,
                        detail=f"File not found: {file_path}",
                    )

                with source_path.open("rb") as src, destination_path.open("wb") as dst:
                    dst.write(src.read())

            return f"{settings.disk_storage_base_url}/{unique_filename}"

        except Exception as e:
            logger.error(f"Failed to upload file to disk storage: {e}")
            raise HTTPException(status_code=500, detail=f"Upload failed: {e!s}") from e

    def _is_base64(self, data: str) -> bool:
        """Check if string is base64 encoded."""
        try:
            if len(data) % 4 != 0:
                return False
            base64.b64decode(data, validate=True)
            return True
        except Exception:
            return False
