from typing import Any

from apps.core.utils.google import (
    GoogleDriveFileContentDict,
    get_google_drive_file_content_dict,
)
from apps.modules.shared.google.services.copy_google_drive_file_service import (
    CopyGoogleDriveFileService,
)
from apps.modules.shared.google.services.show_google_drive_file_service import (
    ShowGoogleDriveFileService,
)
from apps.modules.shared.google.services.update_google_drive_file_service import (
    UpdateGoogleDriveFileService,
)


class GoogleDriveFileController:
    """Google Drive File Controller."""

    async def show(
        self,
        file_id: str,
        show_google_drive_file_service: ShowGoogleDriveFileService,
    ) -> GoogleDriveFileContentDict:
        """Show Google Drive file."""

        file = await show_google_drive_file_service.execute(file_id)

        return get_google_drive_file_content_dict(file)

    async def copy(
        self,
        file_id: str,
        copy_google_drive_file_service: CopyGoogleDriveFileService,
    ) -> dict[str, Any]:
        """Create Google Drive file."""

        return await copy_google_drive_file_service.execute(file_id)

    async def update(
        self,
        file_id: str,
        body: dict[str, Any],
        update_google_drive_file_service: UpdateGoogleDriveFileService,
    ) -> dict[str, Any]:
        """Update Google Drive file."""

        return await update_google_drive_file_service.execute(file_id, body)
