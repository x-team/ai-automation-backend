from typing import Optional

from apps.core.utils.google import GoogleDriveFileContentDict
from apps.modules.quinn.slides.schemas.survey_data_analysis_schema import Slideshow
from apps.modules.quinn.slides.services.create_charts_image_service import (
    CreateChartsImageService,
)


class SlidesChartsImageController:
    """Slides Charts Image Controller."""

    async def create(
        self,
        slides_data: Slideshow,
        source_file_content: GoogleDriveFileContentDict,
        create_charts_image_service: CreateChartsImageService,
        hierarchical_questions: Optional[dict[str, dict[str, str]]] = None,
    ) -> Slideshow:
        """Create charts images."""

        return await create_charts_image_service.execute(
            slides_data,
            source_file_content,
            hierarchical_questions,
        )
