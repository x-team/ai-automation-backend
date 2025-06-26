import os
from pathlib import Path

from fastapi import logger as fastapi_logger

from apps.core.utils.files import (
    extract_text_from_pdf,
    get_embeddings_rag_batch,
    split_text,
)
from apps.modules.shared.rag.infra.sql_alchemy.models.resource_chunks import (
    ResourceChunkModel,
)
from apps.modules.shared.rag.infra.sql_alchemy.models.resources import ResourceModel
from apps.modules.shared.rag.repository_interfaces.resource_chunks_repository_interface import (
    IResourceChunksRepository,
)
from apps.modules.shared.rag.repository_interfaces.resources_repository_interface import (
    IResourcesRepository,
)
from apps.modules.shared.rag.schemas.resource_chunk_schema import (
    ResourceChunkSearchResponse,
)

logger = fastapi_logger.logger


class CreateRAGResourcesService:
    """Create RAG resources service."""

    def __init__(
        self,
        folder_path: str,
        resources_repository: IResourcesRepository[ResourceModel],
        resource_chunks_repository: IResourceChunksRepository[
            ResourceChunkModel,
            ResourceChunkSearchResponse,
        ],
    ) -> None:
        self.folder_path = folder_path
        self.resources_repository = resources_repository
        self.resource_chunks_repository = resource_chunks_repository

    async def execute(self) -> None:
        """Execute the RAG resources service."""

        for filename in os.listdir(self.folder_path):
            if not filename.endswith(".pdf"):
                continue

            pdf_path = Path(self.folder_path) / filename
            resource_name = pdf_path.name

            resource_exists = await self.resources_repository.get_by_name(resource_name)
            if resource_exists:
                logger.info(f"Resource '{resource_name}' already exists. Skipping...")
                continue

            # Extract text from PDF
            content = extract_text_from_pdf(pdf_path)

            # Check for null bytes and handle them
            if "\x00" in content:
                logger.warning(
                    f"Content for resource '{resource_name}' contains null bytes. Cleaning up...",
                )
                content = content.replace("\x00", "")

            # Create resource
            logger.info(f"Processing resource: {resource_name}...")
            resource_created = await self.resources_repository.create(
                ResourceModel(name=resource_name, content=content),
            )

            # Split content into larger chunks with less overlap
            chunks = split_text(content, chunk_size=2000, overlap=100)
            logger.info(f"Split into {len(chunks)} chunks")

            # Process chunks in batches
            batch_size = 100  # Adjust based on your OpenAI rate limits
            embeddings = get_embeddings_rag_batch(chunks, batch_size=batch_size)

            await self.resource_chunks_repository.batch_create(
                [
                    ResourceChunkModel(
                        resource_id=resource_created.id,
                        chunk_index=i,
                        text=chunk,
                        embedding=embedding,
                    )
                    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
                ],
            )
            logger.info(f"Finished processing resource: {resource_name}.\n")
