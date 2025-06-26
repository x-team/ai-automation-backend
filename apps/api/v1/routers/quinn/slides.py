from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.infra.sql_alchemy.dependencies import get_db_session
from apps.modules.quinn.slides.controllers.slides_controller import SlidesController
from apps.modules.quinn.slides.services.create_slides_service import CreateSlidesService

router = APIRouter()

slides_controller = SlidesController()


# Dependency injections
def get_create_slides_service(
    db: AsyncSession = Depends(get_db_session),
) -> CreateSlidesService:
    """Get create slides service."""

    return CreateSlidesService()


# Routes
@router.get("/generate-slides")
async def generate_slides(
    source_file_drive_url: str,
    description_prompt: str,
    structured_questions_file_drive_url: str,
    input_spreadsheet_row: int,
    create_slides_service: CreateSlidesService = Depends(get_create_slides_service),
) -> dict[str, str]:
    """
    Generates slides for Quinn.

    It returns 200 if the slides are generated.
    """

    return await slides_controller.create(
        source_file_drive_url,
        description_prompt,
        structured_questions_file_drive_url,
        input_spreadsheet_row,
        create_slides_service,
    )
