from apps.modules.quinn.llms.services.show_analyze_survey_data_prompt_service import (
    ShowAnalyzeSurveyDataPromptService,
)


class AnalyzeSurveyDataLLMController:
    """Analyze survey data LLM controller."""

    async def show(
        self,
        show_analyze_survey_data_prompt_service: ShowAnalyzeSurveyDataPromptService,
    ) -> str:
        """Show analyze survey data prompt."""

        return await show_analyze_survey_data_prompt_service.execute()
