from typing import Optional

from fastapi import logger as fastapi_logger

from apps.core.utils.google import GoogleDriveFileContentDict

logger = fastapi_logger.logger


class CreateSlidesService:
    """Create Slides Service."""

    def __init__(self) -> None:
        pass

    async def execute(
        self,
        source_file_content: GoogleDriveFileContentDict,
        structure_description: str,
        analyze_survey_data_prompt: str,
        structured_questions_file_content: Optional[GoogleDriveFileContentDict] = None,
    ) -> dict[str, str]:
        """Execute the Create Slides Service."""

        # Get Chart Base 64

        # Upload files to S3

        # Copy Template Slides and change name

        # Replace placeholders

        # Upload Slides to Google Drive

        return {}
