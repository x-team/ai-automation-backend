from typing import Optional

from apps.core.utils.google import GoogleDriveFileContentDict
from apps.modules.quinn.slides.utils.helpers import get_hierarchical_question_structure


class CreateSlidesService:
    """Create Slides Service."""

    def __init__(self) -> None:
        pass

    async def execute(
        self,
        source_file_content: GoogleDriveFileContentDict,
        description_prompt: str,
        input_spreadsheet_row: int,
        structured_questions_file_content: Optional[GoogleDriveFileContentDict] = None,
    ) -> dict[str, str]:
        """Execute the Create Slides Service."""

        # Get the hierarchical questions structure (if any)
        hierarchical_questions = None
        if structured_questions_file_content:
            hierarchical_questions = get_hierarchical_question_structure(
                structured_questions_file_content.data,
            )
            print(hierarchical_questions)  # noqa: T201

        # Prompt into LLM

        # Get Chart Base 64

        # Upload files to S3

        # Copy Template Slides and change name

        # Replace placeholders

        # Upload Slides to Google Drive

        return {}
