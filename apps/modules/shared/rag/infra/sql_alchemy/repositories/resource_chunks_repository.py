from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.utils.files import text_to_vector
from apps.modules.shared.rag.infra.sql_alchemy.models.resource_chunks import (
    ResourceChunkModel,
)
from apps.modules.shared.rag.infra.sql_alchemy.models.resources import ResourceModel
from apps.modules.shared.rag.repository_interfaces.resource_chunks_repository_interface import (
    IResourceChunksRepository,
)
from apps.modules.shared.rag.schemas.resource_chunk_schema import (
    ResourceChunkSearchResponse,
)


class ResourceChunksRepository(
    IResourceChunksRepository[ResourceChunkModel, ResourceChunkSearchResponse],
):
    """Resource chunks repository."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def batch_create(
        self,
        resource_chunks: List[ResourceChunkModel],
    ) -> None:
        """Batch create resource chunks."""

        self.db.add_all(resource_chunks)

    async def search_by_embedding(
        self,
        query: str,
        top_k: int = 5,
        resource_names: Optional[List[str]] = None,
    ) -> List[ResourceChunkSearchResponse]:
        """Search resource chunks by embedding similarity."""

        vector = text_to_vector(query)
        distance_expression = ResourceChunkModel.embedding.l2_distance(vector).label(
            "distance",
        )
        stmt = (
            select(
                ResourceChunkModel.text,
                ResourceChunkModel.chunk_index,
                ResourceModel.name,
                distance_expression,
            )
            .join(ResourceModel, ResourceChunkModel.resource_id == ResourceModel.id)
            .order_by("distance")
            .limit(top_k)
        )

        if resource_names:
            stmt = stmt.where(ResourceModel.name.in_(resource_names))

        query_result = await self.db.execute(stmt)

        results = query_result.mappings().all()
        return [
            ResourceChunkSearchResponse(
                resource_name=row["name"],
                text=row["text"],
                chunk_index=row["chunk_index"],
            )
            for row in results
        ]
