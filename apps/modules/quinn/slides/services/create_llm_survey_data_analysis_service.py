import time  # noqa: I001
from typing import Optional

from fastapi import HTTPException, logger as fastapi_logger

from apps.core.config import settings
from apps.core.utils.google import GoogleDriveFileContentDict
from apps.modules.quinn.slides.schemas.survey_data_analysis_schema import Slideshow

logger = fastapi_logger.logger


class CreateLLMSurveyDataAnalysisService:
    """Create LLM Survey Data Analysis Service."""

    def __init__(self) -> None:
        pass

    async def execute(
        self,
        source_file_content: GoogleDriveFileContentDict,
        structure_description: str,
        analyze_survey_data_prompt: str,
        hierarchical_questions: Optional[dict[str, dict[str, str]]] = None,
    ) -> Slideshow:
        """Execute the Create LLM Survey Data Analysis Service."""

        logger.info("Starting the LLM Survey Data Analysis")
        start_time = time.time()

        response = settings.openai_client.responses.parse(
            model=settings.reasoning_openai_model,
            input=[
                {"role": "system", "content": analyze_survey_data_prompt},
                {
                    "role": "user",
                    "content": f"""
                        `survey_response_data`:
                        {source_file_content.data}

                        `structure_description`:
                        {structure_description}

                        `hierarchical_question_structure`:
                        {hierarchical_questions or ''}

                        `survey_header_columns`:
                        {source_file_content.headers}
                    """,
                },
            ],
            text_format=Slideshow,
        )
        if not response.output_parsed:
            raise HTTPException(status_code=400, detail="No output parsed")

        end_time = time.time()
        logger.info(
            f"LLM Survey Data Analysis completed in {end_time - start_time} seconds",
        )

        return response.output_parsed
