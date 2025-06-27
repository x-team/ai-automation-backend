from typing import Optional  # noqa: I001
from apps.core.providers.storage_provider.repository_interfaces.storage_repository_interface import (
    IStorageProvider,
)
from apps.core.utils.google import GoogleDriveFileContentDict
from apps.modules.quinn.slides.schemas.survey_data_analysis_schema import Slideshow
from apps.modules.quinn.slides.utils.charts import process_slides_and_generate_charts


class CreateChartsImageService:
    """Create Charts Image Service."""

    def __init__(self, storage_provider: IStorageProvider) -> None:
        self.storage_provider = storage_provider

    async def execute(
        self,
        slides_data: Slideshow,
        source_file_content: GoogleDriveFileContentDict,
        hierarchical_questions: Optional[dict[str, dict[str, str]]] = None,
    ) -> Slideshow:
        """Execute the Create Charts Image Service."""

        valid_survey_data = []
        for row in source_file_content.data:
            copy_row = row.copy()

            for dependent_column, rule in (hierarchical_questions or {}).items():
                depends_on_column = rule.get("dependsOn")
                required_value = rule.get("value", "").lower()

                if (
                    depends_on_column
                    and str(copy_row.get(depends_on_column, "")).lower()
                    != str(required_value)
                    and dependent_column in copy_row
                ):
                    del copy_row[dependent_column]

            valid_survey_data.append(copy_row)

        # Generate charts in base64
        generated_charts_base64 = process_slides_and_generate_charts(
            slides_data.slides,
            valid_survey_data,
        )

        # Upload charts to S3
        for chart in generated_charts_base64:
            await self.storage_provider.upload_file(
                chart["data"],
                f"{chart['title']}.png",
            )

        # Return Charts URLs
        index_to_title = {
            item["index"]: item["title"]
            for item in generated_charts_base64
            if "index" in item and "title" in item
        }

        for i, slide in enumerate(slides_data.slides):
            title = index_to_title.get(i)
            if not title:
                continue
            slide.image_url = f"https://ai-automation-team.s3.us-east-1.amazonaws.com/quinn/{title}.png"

        return slides_data
