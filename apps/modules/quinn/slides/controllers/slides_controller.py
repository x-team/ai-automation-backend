from typing import Optional

from apps.core.utils.google import GoogleDriveFileContentDict
from apps.modules.quinn.slides.services.create_slides_service import CreateSlidesService


class SlidesController:
    """Slides Controller."""

    async def create(
        self,
        source_file_content: GoogleDriveFileContentDict,
        description_prompt: str,
        input_spreadsheet_row: int,
        create_slides_service: CreateSlidesService,
        structured_questions_file_content: Optional[GoogleDriveFileContentDict] = None,
    ) -> dict[str, str]:
        """Create slides."""

        return await create_slides_service.execute(
            source_file_content,
            description_prompt,
            input_spreadsheet_row,
            structured_questions_file_content,
        )
