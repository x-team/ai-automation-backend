from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IResourcesRepository(Generic[T]):
    """Resources repository interface."""

    @abstractmethod
    async def create(self, resource: T) -> T:
        """Create resource."""

    @abstractmethod
    async def get_by_name(self, name: str) -> T | None:
        """Get resource by name."""
