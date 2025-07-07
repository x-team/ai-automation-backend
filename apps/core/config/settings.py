import enum
import os
from pathlib import Path
from tempfile import gettempdir
from typing import Any, Literal

from openai import AsyncOpenAI, OpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

from apps.core.utils.google import get_google_drive_service, get_google_slides_service

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    port: int = int(os.getenv("BACKEND_PORT", "8000"))

    db_host: str = os.getenv("POSTGRES_HOST", "127.0.0.1")
    db_echo: bool = False

    # Quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = os.getenv("RELOAD", "False") == "True"

    # Current environment
    environment: str = os.getenv("ENVIRONMENT", "dev")

    log_level: LogLevel = LogLevel.INFO

    # Quinn API key for authentication
    quinn_api_key: str = os.getenv("QUINN_API_KEY", "")

    # Variables for Postgres
    postgres_host: str = os.getenv("POSTGRES_HOST", "127.0.0.1")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_base: str = os.getenv("POSTGRES_DB", "postgres")
    postgres_pass: str = os.getenv("POSTGRES_PASSWORD", "password")

    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_organization_id: str = os.getenv("OPENAI_ORGANIZATION_ID", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    base_openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    reasoning_openai_model: str = os.getenv("OPENAI_REASONING_MODEL", "o3-mini")

    # Storage provider
    storage_provider: Literal["disk", "s3"] = os.getenv("STORAGE_PROVIDER", "disk")  # type: ignore[assignment]

    # AWS S3 settings
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME", "ai-automation-team")
    s3_bucket_folder: str = os.getenv("S3_BUCKET_FOLDER", "quinn")

    # Google Cloud
    google_cloud_impersonated_account: str = os.getenv(
        "GOOGLE_CLOUD_IMPERSONATED_ACCOUNT",
        "angie@x-team.com",
    )

    # Disk storage settings
    disk_storage_path: str = os.getenv("DISK_STORAGE_PATH", "storage/uploads")
    disk_storage_base_url: str = os.getenv(
        "DISK_STORAGE_BASE_URL",
        "http://localhost:8000/static",
    )

    # Quinn Settings
    quinn_make_scenario_url: str = os.getenv("QUINN_MAKE_SCENARIO_URL", "")
    quinn_google_drive_template_slides_id: str = os.getenv(
        "QUINN_GOOGLE_DRIVE_TEMPLATE_SLIDES_ID",
        "102Thay7QPpYp4YIl2osChQPrN4yb-oPy1h7O5ZBeCMs",
    )

    @property
    def openai_client(self) -> OpenAI:
        """OpenAI client."""
        return OpenAI(
            api_key=self.openai_api_key,
            organization=self.openai_organization_id,
        )

    @property
    def openai_client_async(self) -> AsyncOpenAI:
        """Async OpenAI client."""
        return AsyncOpenAI(
            api_key=self.openai_api_key,
            organization=self.openai_organization_id,
        )

    @property
    def google_drive_service(self) -> Any:
        """Google Drive service."""
        return get_google_drive_service(self.google_cloud_impersonated_account)

    @property
    def google_slides_service(self) -> Any:
        """Google Slides service."""
        return get_google_slides_service()

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.postgres_host,
            port=int(self.postgres_port),
            user=self.postgres_user,
            password=self.postgres_pass,
            path=f"/{self.postgres_base}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
