from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.infra.sql_alchemy.dependencies import get_db_session
from apps.modules.shared.rag.controllers.rag_resources_controller import (
    RAGResourcesController,
)
from apps.modules.shared.rag.infra.sql_alchemy.repositories.resource_chunks_repository import (
    ResourceChunksRepository,
)
from apps.modules.shared.rag.infra.sql_alchemy.repositories.resources_repository import (
    ResourcesRepository,
)
from apps.modules.shared.rag.services.create_rag_resources import (
    CreateRAGResourcesService,
)
from apps.modules.shared.rag.services.list_resource_chunks import (
    ListResourceChunksService,
)

router = APIRouter()

rag_resources_controller = RAGResourcesController()


# Dependency injections
def get_rag_resources_service(
    db: AsyncSession = Depends(get_db_session),
) -> CreateRAGResourcesService:
    """Get RAG resources service."""

    resources_repository = ResourcesRepository(db)
    resource_chunks_repository = ResourceChunksRepository(db)

    return CreateRAGResourcesService(
        folder_path="apps/core/rag_data/resources",
        resources_repository=resources_repository,
        resource_chunks_repository=resource_chunks_repository,
    )


def get_list_resource_chunks_service(
    db: AsyncSession = Depends(get_db_session),
) -> ListResourceChunksService:
    """Get list resource chunks service."""

    resource_chunks_repository = ResourceChunksRepository(db)

    return ListResourceChunksService(resource_chunks_repository)


# Routes
@router.get("/add-resources", status_code=201)
async def add_resources(
    rag_resources_service: CreateRAGResourcesService = Depends(
        get_rag_resources_service,
    ),
) -> None:
    """
    Adds resources to the database.

    It returns 201 if the resources were added successfully
    """

    await rag_resources_controller.create(
        rag_resources_service,
    )
