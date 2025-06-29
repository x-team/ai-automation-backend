from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException

from apps.core.config import settings
from apps.core.providers.storage_provider import get_storage_provider
from apps.core.utils.google import get_google_drive_id
from apps.modules.quinn.llms.controllers.analyze_survey_data_controller import (
    AnalyzeSurveyDataLLMController,
)
from apps.modules.quinn.llms.services.show_analyze_survey_data_prompt_service import (
    ShowAnalyzeSurveyDataPromptService,
)
from apps.modules.quinn.slides.controllers.slides_charts_image_controller import (
    SlidesChartsImageController,
)
from apps.modules.quinn.slides.controllers.slides_survey_data_analysis_controller import (
    SlidesSurveyDataAnalysisController,
)
from apps.modules.quinn.slides.schemas.survey_data_analysis_schema import Slideshow
from apps.modules.quinn.slides.services.create_charts_image_service import (
    CreateChartsImageService,
)
from apps.modules.quinn.slides.services.create_llm_survey_data_analysis_service import (
    CreateLLMSurveyDataAnalysisService,
)
from apps.modules.quinn.slides.utils.google_slides import (
    create_google_slides_presentation,
)
from apps.modules.quinn.slides.utils.helpers import get_hierarchical_question_structure
from apps.modules.shared.google.controllers.google_drive_file_controller import (
    GoogleDriveFileController,
)
from apps.modules.shared.google.controllers.google_slides_file_controller import (
    GoogleSlidesFileController,
)
from apps.modules.shared.google.services.copy_google_drive_file_service import (
    CopyGoogleDriveFileService,
)
from apps.modules.shared.google.services.show_google_drive_file_service import (
    ShowGoogleDriveFileService,
)
from apps.modules.shared.google.services.show_google_slides_file_service import (
    ShowGoogleSlidesFileService,
)
from apps.modules.shared.google.services.update_google_drive_file_service import (
    UpdateGoogleDriveFileService,
)
from apps.modules.shared.google.services.update_google_slides_file_service import (
    UpdateGoogleSlidesFileService,
)

router = APIRouter()

analyze_survey_data_llm_controller = AnalyzeSurveyDataLLMController()
slides_survey_data_analysis_controller = SlidesSurveyDataAnalysisController()
slides_charts_image_controller = SlidesChartsImageController()
google_drive_file_controller = GoogleDriveFileController()
google_slides_file_controller = GoogleSlidesFileController()


# Dependency injections
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


def get_update_google_drive_file_service() -> UpdateGoogleDriveFileService:
    """Get update google drive file service."""

    return UpdateGoogleDriveFileService()


def get_update_google_slides_file_service() -> UpdateGoogleSlidesFileService:
    """Get update google slides file service."""

    return UpdateGoogleSlidesFileService()


def get_show_google_slides_file_service() -> ShowGoogleSlidesFileService:
    """Get show google slides file service."""

    return ShowGoogleSlidesFileService()


def get_copy_google_drive_file_service() -> CopyGoogleDriveFileService:
    """Get copy google drive file service."""

    return CopyGoogleDriveFileService()


# Routes
@router.post("/generate-slides", response_model=Slideshow)
async def generate_slides(
    source_file_drive_url: str,
    description_prompt: str,
    input_spreadsheet_row: int,
    structured_questions_file_drive_url: Optional[str] = None,
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
    update_google_drive_file_service: UpdateGoogleDriveFileService = Depends(
        get_update_google_drive_file_service,
    ),
    update_google_slides_file_service: UpdateGoogleSlidesFileService = Depends(
        get_update_google_slides_file_service,
    ),
    show_google_slides_file_service: ShowGoogleSlidesFileService = Depends(
        get_show_google_slides_file_service,
    ),
    copy_google_drive_file_service: CopyGoogleDriveFileService = Depends(
        get_copy_google_drive_file_service,
    ),
) -> Slideshow:
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

    # Get the hierarchical questions structure (if any)
    hierarchical_questions = None
    if structured_questions_file_content:
        hierarchical_questions = get_hierarchical_question_structure(
            structured_questions_file_content.data,
        )

    # Create slides for survey data analysis
    slides_data = await slides_survey_data_analysis_controller.create(
        source_file_content,
        description_prompt,
        analyze_survey_data_prompt,
        create_llm_survey_data_analysis_service,
        hierarchical_questions,
    )

    # Create charts images
    slides_data = await slides_charts_image_controller.create(
        slides_data,
        source_file_content,
        create_charts_image_service,
        hierarchical_questions,
    )

    # Drive - Copy Template Slides
    google_drive_copy_file = await google_drive_file_controller.copy(
        source_file_drive_id,
        copy_google_drive_file_service,
    )
    if not google_drive_copy_file or not google_drive_copy_file["id"]:
        raise HTTPException(status_code=404, detail="Template slides file not found")

    # Drive - Update file name
    await google_drive_file_controller.update(
        google_drive_copy_file.get("id", ""),
        {
            "name": f"Quinn_presentation_{google_drive_copy_file.get('createdTime')}",
        },
        update_google_drive_file_service,
    )

    # Slides - Find presentation
    google_slides_find_presentation = await google_slides_file_controller.show(
        google_drive_copy_file["id"],
        show_google_slides_file_service,
    )
    if not google_slides_find_presentation or not google_slides_find_presentation["id"]:
        raise HTTPException(status_code=404, detail="Slides file not found")

    # Slides - Upload Slides to Google Drive
    await google_slides_file_controller.update(
        google_slides_find_presentation["id"],
        {
            "requests": create_google_slides_presentation(
                source_file_content.data,
                google_slides_find_presentation["id"],
                google_slides_find_presentation["layouts"],
            ),
        },
        update_google_slides_file_service,
    )

    # Update Make Scenario
    async with httpx.AsyncClient() as client:
        await client.post(
            settings.quinn_make_scenario_url,
            data={
                "presentation_url": f"https://docs.google.com/presentation/d/{google_drive_copy_file['id']}/view",
                "row": input_spreadsheet_row,
            },
            timeout=30,
        )

    return slides_data
