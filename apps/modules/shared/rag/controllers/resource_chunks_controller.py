from typing import List

from apps.modules.shared.rag.schemas.resource_chunk_schema import (
    ResourceChunkSearchResponse,
)
from apps.modules.shared.rag.services.list_resource_chunks import (
    ListResourceChunksService,
)


class ResourceChunksController:
    """Resource chunks controller."""

    async def list(
        self,
        list_resource_chunks_service: ListResourceChunksService,
        query: str,
    ) -> List[ResourceChunkSearchResponse]:
        """List resources."""

        return await list_resource_chunks_service.execute(query)

    # async def create(
    #     self,
    # ) -> None:
    #    pass

    # def show(self) -> T:
    #     pass

    # def delete(self) -> T:
    #     pass

    # def update(self) -> T:
    #     pass
