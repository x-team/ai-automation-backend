from apps.modules.quinn.slides.services.create_slides_service import CreateSlidesService


class SlidesController:
    """Slides Controller."""

    async def create(
        self,
        source_file_drive_url: str,
        description_prompt: str,
        structured_questions_file_drive_url: str,
        input_spreadsheet_row: int,
        create_slides_service: CreateSlidesService,
    ) -> dict[str, str]:
        """Create slides."""

        return await create_slides_service.execute(
            source_file_drive_url,
            description_prompt,
            structured_questions_file_drive_url,
            input_spreadsheet_row,
        )
