from typing import List

from apps.modules.shared.rag.infra.sql_alchemy.models.resource_chunks import (
    ResourceChunkModel,
)
from apps.modules.shared.rag.repository_interfaces.resource_chunks_repository_interface import (
    IResourceChunksRepository,
)
from apps.modules.shared.rag.schemas.resource_chunk_schema import (
    ResourceChunkSearchResponse,
)


class ListResourceChunksService:
    """List resource chunks service."""

    def __init__(
        self,
        resource_chunks_repository: IResourceChunksRepository[
            ResourceChunkModel,
            ResourceChunkSearchResponse,
        ],
    ) -> None:
        self.resource_chunks_repository = resource_chunks_repository

    async def execute(
        self,
        query: str,
        chunk_top_k: int = 5,
    ) -> List[ResourceChunkSearchResponse]:
        """Execute the list resources service."""

        resource_chunks = await self.resource_chunks_repository.search_by_embedding(
            query=query,
            top_k=chunk_top_k,
        )
        return [
            ResourceChunkSearchResponse.model_validate(resource_chunk)
            for resource_chunk in resource_chunks
        ]
