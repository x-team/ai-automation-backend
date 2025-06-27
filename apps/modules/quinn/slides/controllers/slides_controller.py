from typing import Optional

from apps.core.utils.google import GoogleDriveFileContentDict
from apps.modules.quinn.slides.services.create_charts_image_service import (
    CreateChartsImageService,
)
from apps.modules.quinn.slides.services.create_llm_survey_data_analysis_service import (
    CreateLLMSurveyDataAnalysisService,
)
from apps.modules.quinn.slides.services.create_slides_service import CreateSlidesService
from apps.modules.quinn.slides.utils.helpers import get_hierarchical_question_structure


class SlidesController:
    """Slides Controller."""

    async def create(
        self,
        source_file_content: GoogleDriveFileContentDict,
        structure_description: str,
        analyze_survey_data_prompt: str,
        create_slides_service: CreateSlidesService,
        create_llm_survey_data_analysis_service: CreateLLMSurveyDataAnalysisService,
        create_charts_image_service: CreateChartsImageService,
        structured_questions_file_content: Optional[GoogleDriveFileContentDict] = None,
    ) -> dict[str, str]:
        """Create slides."""

        # Get the hierarchical questions structure (if any)
        hierarchical_questions = None
        if structured_questions_file_content:
            hierarchical_questions = get_hierarchical_question_structure(
                structured_questions_file_content.data,
            )

        slides_data = await create_llm_survey_data_analysis_service.execute(
            source_file_content,
            structure_description,
            analyze_survey_data_prompt,
            hierarchical_questions,
        )

        slides_data = await create_charts_image_service.execute(
            slides_data,
            source_file_content,
            hierarchical_questions,
        )

        return await create_slides_service.execute(
            source_file_content,
            structure_description,
            analyze_survey_data_prompt,
            structured_questions_file_content,
        )
