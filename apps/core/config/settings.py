import enum
import os
from pathlib import Path
from tempfile import gettempdir

from openai import OpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

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

    @property
    def openai_client(self) -> OpenAI:
        """OpenAI client."""
        return OpenAI(
            api_key=self.openai_api_key,
            organization=self.openai_organization_id,
        )

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
