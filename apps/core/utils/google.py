import csv
import io
import os
import re
from typing import Any, Optional

from fastapi import logger as fastapi_logger
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from pydantic import BaseModel

logger = fastapi_logger.logger


SERVICE_ACCOUNT_FILE = "apps/core/config/secrets/service_account.json"


# GOOGLE DRIVE
class GoogleDriveFileContentDict(BaseModel):
    """Google Drive File Content Dict."""

    headers: list[str]
    data: list[dict[str, Any]]


def get_google_drive_service(impersonated_account: str) -> Any:
    """Get the drive service."""

    creds = None

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/drive"],
            subject=impersonated_account,
        )
    except Exception as err:
        logger.error("Error getting drive service: %s", err)

    try:
        return build("drive", "v3", credentials=creds)
    except Exception as err:
        logger.error("Error building drive service: %s", err)


def get_google_drive_id(url: str) -> Optional[str]:
    """Get the Google Drive ID from the URL."""

    regex = r"/d/([a-zA-Z0-9_-]+)"
    match = re.search(regex, url)

    return match.group(1) if match else None


def get_google_drive_file_content_dict(
    file: dict[str, str],
) -> GoogleDriveFileContentDict:
    """Get the Google Drive file content."""

    google_drive_service = get_google_drive_service(
        os.getenv(
            "GOOGLE_CLOUD_IMPERSONATED_ACCOUNT",
            "angie@x-team.com",
        ),
    )
    mime_type = file.get("mimeType", "")
    file_id = file.get("id", "")

    if mime_type == "application/vnd.google-apps.spreadsheet":
        request = google_drive_service.files().export_media(
            fileId=file_id,
            mimeType="text/csv",
        )
    else:
        request = google_drive_service.files().get_media(
            fileId=file_id,
            supportsAllDrives=True,
        )

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        logger.info(f"Download in progress: {int(status.progress() * 100)}%")

    fh.seek(0)
    csv_content = fh.read()
    try:
        decoded_content = csv_content.decode("utf-8")
    except UnicodeDecodeError:
        logger.info("utf-8 decoding failed, falling back to latin-1")
        decoded_content = csv_content.decode("latin-1")

    csv_file = io.StringIO(decoded_content)
    reader = csv.reader(csv_file)
    headers = next(reader)

    cleaned_headers = [
        header.strip().replace("\n", " ").replace("  ", " ") for header in headers
    ]
    data_body = []
    for row in reader:
        if len(row) == len(cleaned_headers):
            row_object = dict(zip(cleaned_headers, row))
            data_body.append(row_object)
        else:
            logger.info(
                f"Skipping malformed row. Expected {len(cleaned_headers)} columns, but found {len(row)}.",
            )

    return GoogleDriveFileContentDict(
        headers=cleaned_headers,
        data=data_body,
    )


# GOOGLE SLIDES
def get_google_slides_service() -> Any:
    """Get the slides service."""

    creds = None

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/presentations"],
        )
    except Exception as err:
        logger.error("Error getting slides service: %s", err)

    try:
        return build("slides", "v1", credentials=creds)
    except Exception as err:
        logger.error("Error building slides service: %s", err)
