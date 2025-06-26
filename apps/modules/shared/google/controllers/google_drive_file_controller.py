from apps.core.utils.google import (
    GoogleDriveFileContentDict,
    get_google_drive_file_content_dict,
)
from apps.modules.shared.google.services.show_google_drive_file_service import (
    ShowGoogleDriveFileService,
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
