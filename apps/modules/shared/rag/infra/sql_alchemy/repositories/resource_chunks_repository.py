from typing import List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.utils.files import text_to_vector
from apps.modules.shared.rag.infra.sql_alchemy.models.resource_chunks import (
    ResourceChunkModel,
)
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
        await self.db.commit()

    async def search_by_embedding(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[ResourceChunkSearchResponse]:
        """Search resource chunks by embedding similarity."""

        stmt = text(
            """
            SELECT rc.*, r.name, rc.embedding <-> cast(:query as vector) as distance
            FROM resource_chunks rc
            JOIN resources r ON rc.resource_id = r.id
            ORDER BY distance ASC
            LIMIT :top_k
            """,
        )

        vector = text_to_vector(query)
        query_result = await self.db.execute(
            stmt,
            {"query": vector, "top_k": top_k},
        )

        results = query_result.mappings().all()
        return [
            ResourceChunkSearchResponse(
                resource_name=row["name"],
                text=row["text"],
                chunk_index=row["chunk_index"],
            )
            for row in results
        ]
