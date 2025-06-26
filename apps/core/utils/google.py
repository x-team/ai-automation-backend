from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_drive_service() -> Any:
    """Get the drive service."""

    creds = None
    if Path("token.json").exists():
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with Path("token.json").open("w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)
