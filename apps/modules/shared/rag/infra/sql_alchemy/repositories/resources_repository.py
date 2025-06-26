from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.modules.shared.rag.infra.sql_alchemy.models.resources import ResourceModel
from apps.modules.shared.rag.repository_interfaces.resources_repository_interface import (
    IResourcesRepository,
)


class ResourcesRepository(IResourcesRepository[ResourceModel]):
    """Resources repository."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, resource: ResourceModel) -> ResourceModel:
        """Create resource."""

        self.db.add(resource)
        await self.db.commit()
        await self.db.refresh(resource)

        return resource

    async def get_by_name(self, name: str) -> ResourceModel | None:
        """Get resource by name."""

        result = await self.db.execute(
            select(ResourceModel).where(ResourceModel.name == name),
        )
        return result.unique().scalar_one_or_none()
