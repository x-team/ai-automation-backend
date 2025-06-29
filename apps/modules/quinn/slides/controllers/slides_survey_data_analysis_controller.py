from typing import Optional

from apps.core.utils.google import GoogleDriveFileContentDict
from apps.modules.quinn.slides.schemas.survey_data_analysis_schema import Slideshow
from apps.modules.quinn.slides.services.create_llm_survey_data_analysis_service import (
    CreateLLMSurveyDataAnalysisService,
)


class SlidesSurveyDataAnalysisController:
    """Slides Survey Data Analysis Controller."""

    async def create(
        self,
        source_file_content: GoogleDriveFileContentDict,
        structure_description: str,
        analyze_survey_data_prompt: str,
        create_llm_survey_data_analysis_service: CreateLLMSurveyDataAnalysisService,
        hierarchical_questions: Optional[dict[str, dict[str, str]]] = None,
    ) -> Slideshow:
        """Create slides for survey data analysis."""

        return await create_llm_survey_data_analysis_service.execute(
            source_file_content,
            structure_description,
            analyze_survey_data_prompt,
            hierarchical_questions,
        )
