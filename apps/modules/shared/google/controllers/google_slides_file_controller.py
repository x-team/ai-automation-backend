from typing import Any

from apps.modules.shared.google.services.show_google_slides_file_service import (
    ShowGoogleSlidesFileService,
)
from apps.modules.shared.google.services.update_google_slides_file_service import (
    UpdateGoogleSlidesFileService,
)


class GoogleSlidesFileController:
    """Google Slides File Controller."""

    async def show(
        self,
        presentation_id: str,
        show_google_slides_file_service: ShowGoogleSlidesFileService,
    ) -> dict[str, Any]:
        """Show Google Slides file."""

        return await show_google_slides_file_service.execute(presentation_id)

    async def update(
        self,
        presentation_id: str,
        body: dict[str, Any],
        update_google_slides_file_service: UpdateGoogleSlidesFileService,
    ) -> dict[str, Any]:
        """Update Google Slides file."""

        return await update_google_slides_file_service.execute(presentation_id, body)
