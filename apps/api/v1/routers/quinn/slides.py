from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.config import settings
from apps.core.infra.sql_alchemy.dependencies import get_db_session
from apps.core.providers.storage_provider import get_storage_provider
from apps.core.utils.google import get_google_drive_id
from apps.modules.quinn.llms.controllers.analyze_survey_data_controller import (
    AnalyzeSurveyDataLLMController,
)
from apps.modules.quinn.llms.services.show_analyze_survey_data_prompt_service import (
    ShowAnalyzeSurveyDataPromptService,
)
from apps.modules.quinn.slides.controllers.slides_controller import SlidesController
from apps.modules.quinn.slides.services.create_charts_image_service import (
    CreateChartsImageService,
)
from apps.modules.quinn.slides.services.create_llm_survey_data_analysis_service import (
    CreateLLMSurveyDataAnalysisService,
)
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
analyze_survey_data_llm_controller = AnalyzeSurveyDataLLMController()


# Dependency injections
def get_create_slides_service(
    db: AsyncSession = Depends(get_db_session),
) -> CreateSlidesService:
    """Get create slides service."""

    return CreateSlidesService()


def get_show_google_drive_file_service() -> ShowGoogleDriveFileService:
    """Get show google drive file service."""

    return ShowGoogleDriveFileService()


def get_show_analyze_survey_data_prompt_service() -> ShowAnalyzeSurveyDataPromptService:
    """Get show analyze survey data prompt service."""

    return ShowAnalyzeSurveyDataPromptService()


def get_create_llm_survey_data_analysis_service() -> CreateLLMSurveyDataAnalysisService:
    """Get create LLM survey data analysis service."""

    return CreateLLMSurveyDataAnalysisService()


def get_create_charts_image_service() -> CreateChartsImageService:
    """Get create charts image service."""

    storage_provider = get_storage_provider(settings.storage_provider)

    return CreateChartsImageService(storage_provider)


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
    show_analyze_survey_data_prompt_service: ShowAnalyzeSurveyDataPromptService = Depends(
        get_show_analyze_survey_data_prompt_service,
    ),
    create_llm_survey_data_analysis_service: CreateLLMSurveyDataAnalysisService = Depends(
        get_create_llm_survey_data_analysis_service,
    ),
    create_charts_image_service: CreateChartsImageService = Depends(
        get_create_charts_image_service,
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

    # Get the analyze survey data prompt
    analyze_survey_data_prompt = await analyze_survey_data_llm_controller.show(
        show_analyze_survey_data_prompt_service,
    )

    # Break down the process into smaller controllers
    await slides_controller.create(
        source_file_content,
        description_prompt,
        analyze_survey_data_prompt,
        create_slides_service,
        create_llm_survey_data_analysis_service,
        create_charts_image_service,
        structured_questions_file_content,
    )

    return {"message": "Slides generated successfully"}
