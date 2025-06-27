from abc import abstractmethod


class IStorageProvider:
    """Storage provider interface."""

    @abstractmethod
    async def upload_file(self, file_path: str, file_name: str) -> str:
        """Upload a file to the storage provider."""
