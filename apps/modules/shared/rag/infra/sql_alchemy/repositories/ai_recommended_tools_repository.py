from typing import List

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.modules.shared.rag.infra.sql_alchemy.models.ai_recommended_tools import (
    AIRecommendedToolModel,
)
from apps.modules.shared.rag.repository_interfaces.ai_recommended_tools_repository_interface import (
    IAIRecommendedToolsRepository,
)


class AIRecommendedToolsRepository(
    IAIRecommendedToolsRepository[AIRecommendedToolModel],
):
    """AI Recommended Tools repository."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        ai_recommended_tool: AIRecommendedToolModel,
    ) -> AIRecommendedToolModel:
        """Create AI recommended tool."""

        self.db.add(ai_recommended_tool)
        await self.db.commit()
        await self.db.refresh(ai_recommended_tool)

        return ai_recommended_tool

    async def batch_create(
        self,
        ai_recommended_tools: List[AIRecommendedToolModel],
    ) -> None:
        """Create AI recommended tools."""

        self.db.add_all(ai_recommended_tools)
        await self.db.commit()

    async def get_all_context_embeddings(self) -> List[str]:
        """Get all context embeddings."""

        context_embeddings = await self.db.execute(
            select(AIRecommendedToolModel.embedding).distinct(),
        )
        return list(context_embeddings.scalars().all())

    async def get_by_ids(self, ids: List[UUID4]) -> List[AIRecommendedToolModel]:
        """Get by ids."""

        tools = await self.db.execute(
            select(AIRecommendedToolModel).filter(AIRecommendedToolModel.id.in_(ids)),
        )
        return list(tools.scalars().unique().all())

    async def get_all(self) -> List[AIRecommendedToolModel]:
        """Get all tools."""

        tools = await self.db.execute(
            select(AIRecommendedToolModel),
        )
        return list(tools.scalars().unique().all())
