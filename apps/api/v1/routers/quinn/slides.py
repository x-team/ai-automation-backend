from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.infra.sql_alchemy.dependencies import get_db_session
from apps.core.utils.google import get_google_drive_id
from apps.modules.quinn.slides.controllers.slides_controller import SlidesController
from apps.modules.quinn.slides.services.create_slides_service import CreateSlidesService
from apps.modules.shared.google.controllers.google_drive_file_controller import (
    GoogleDriveFileController,
)
from apps.modules.shared.google.services.show_google_drive_file_service import (
    ShowGoogleDriveFileService,
)

router = APIRouter()

slides_controller = SlidesController()
google_drive_file_controller = GoogleDriveFileController()


# Dependency injections
def get_create_slides_service(
    db: AsyncSession = Depends(get_db_session),
) -> CreateSlidesService:
    """Get create slides service."""

    return CreateSlidesService()


def get_show_google_drive_file_service() -> ShowGoogleDriveFileService:
    """Get show google drive file service."""

    return ShowGoogleDriveFileService()


# Routes
@router.post("/generate-slides")
async def generate_slides(
    source_file_drive_url: str,
    description_prompt: str,
    input_spreadsheet_row: int,
    structured_questions_file_drive_url: Optional[str] = None,
    create_slides_service: CreateSlidesService = Depends(get_create_slides_service),
    show_google_drive_file_service: ShowGoogleDriveFileService = Depends(
        get_show_google_drive_file_service,
    ),
) -> dict[str, str]:
    """
    Generates slides for Quinn.

    It returns 200 if the slides are generated.
    """

    source_file_drive_id = get_google_drive_id(source_file_drive_url)
    if not source_file_drive_id:
        raise HTTPException(status_code=400, detail="Invalid source file drive URL")

    # Get the dict content of the source file
    source_file_content = await google_drive_file_controller.show(
        source_file_drive_id,
        show_google_drive_file_service,
    )

    # Get the structured questions from the structured questions file (if any)
    structured_questions_file_content = None
    if structured_questions_file_drive_url:
        structured_questions_file_content = await google_drive_file_controller.show(
            structured_questions_file_drive_url,
            show_google_drive_file_service,
        )

    await slides_controller.create(
        source_file_content,
        description_prompt,
        input_spreadsheet_row,
        create_slides_service,
        structured_questions_file_content,
    )

    return {"message": "Slides generated successfully"}
