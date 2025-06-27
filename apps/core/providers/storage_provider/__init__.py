from typing import Literal

from apps.core.providers.storage_provider.repositories.disk_storage_repository import (
    DiskStorageRepository,
)
from apps.core.providers.storage_provider.repositories.s3_storage_repository import (
    S3StorageRepository,
)
from apps.core.providers.storage_provider.repository_interfaces.storage_repository_interface import (
    IStorageProvider,
)

options = {
    "s3": S3StorageRepository,
    "disk": DiskStorageRepository,
}


def get_storage_provider(type: Literal["s3", "disk"]) -> IStorageProvider:
    """Get the storage provider."""

    storage_provider = options.get(type)
    if not storage_provider:
        raise ValueError(f"Storage provider {type} not found")

    return storage_provider()
