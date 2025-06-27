import base64
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException
from fastapi import logger as fastapi_logger

from apps.core.config import settings
from apps.core.providers.storage_provider.repository_interfaces.storage_repository_interface import (
    IStorageProvider,
)

logger = fastapi_logger.logger


class S3StorageRepository(IStorageProvider):
    """S3 storage repository."""

    def __init__(self) -> None:
        """Initialize S3 client."""
        try:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region,
            )
        except NoCredentialsError as e:
            logger.error("AWS credentials not found")
            raise HTTPException(
                status_code=500,
                detail="AWS credentials not configured",
            ) from e

    async def upload_file(self, file_path: str, file_name: str) -> str:
        """Upload a file to the S3 storage provider.

        Args:
            file_path: Either a file path on disk or base64 encoded file data
            file_name: The name to use for the uploaded file

        Returns:
            The public URL of the uploaded file
        """
        try:
            file_key = f"{settings.s3_bucket_folder}/{file_name}"

            if self._is_base64(file_path):
                file_data = base64.b64decode(file_path)

                logger.info(f"Uploading base64 file: {file_name}")
                self.s3_client.put_object(
                    Bucket=settings.s3_bucket_name,
                    Key=file_key,
                    Body=file_data,
                    ContentType=self._get_content_type(file_name),
                )
            else:
                if not Path(file_path).exists():
                    raise HTTPException(
                        status_code=404,
                        detail=f"File not found: {file_path}",
                    )

                with Path(file_path).open("rb") as file_obj:
                    self.s3_client.upload_fileobj(
                        file_obj,
                        settings.s3_bucket_name,
                        file_key,
                        ExtraArgs={"ContentType": self._get_content_type(file_name)},
                    )

            return f"https://{settings.s3_bucket_name}.s3.{settings.aws_region}.amazonaws.com/{file_key}"

        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file: {e!s}",
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error during S3 upload: {e}")
            raise HTTPException(status_code=500, detail=f"Upload failed: {e!s}") from e

    def _is_base64(self, data: str) -> bool:
        """Check if string is base64 encoded."""

        try:
            if len(data) % 4 != 0:
                return False
            base64.b64decode(data, validate=True)
            return True
        except Exception:
            return False

    def _get_content_type(self, file_name: str) -> str:
        """Get content type based on file extension."""

        extension = file_name.lower().split(".")[-1]
        content_types = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "pdf": "application/pdf",
            "txt": "text/plain",
            "csv": "text/csv",
            "json": "application/json",
        }
        return content_types.get(extension, "application/octet-stream")
