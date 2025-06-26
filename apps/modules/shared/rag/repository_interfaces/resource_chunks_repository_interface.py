from abc import abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")
Y = TypeVar("Y")


class IResourceChunksRepository(Generic[T, Y]):
    """Resource chunks repository interface."""

    @abstractmethod
    async def batch_create(
        self,
        resource_chunks: List[T],
    ) -> None:
        """Batch create resource chunks."""

    @abstractmethod
    async def search_by_embedding(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Y]:
        """Search resource chunks by embedding similarity."""
