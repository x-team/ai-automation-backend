import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_slides(client: AsyncClient) -> None:
    """Test slides."""

    response = await client.post(
        "/quinn/slides",
        json={
            "source_file_drive_url": "https://drive.google.com/file/d/1234567890/view?usp=sharing",
            "description_prompt": "Test description",
            "input_spreadsheet_row": 1,
            "structured_questions_file_drive_url": "https://drive.google.com/file/d/1234567890/view?usp=sharing",
        },
    )

    assert response.status_code == 200
