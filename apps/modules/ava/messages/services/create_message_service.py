from fastapi import logger as fastapi_logger

from apps.modules.ava.messages.infra.crew_ai.agents.knowledge_researcher import (
    KnowledgeResearcher,
)
from apps.modules.ava.messages.infra.crew_ai.agents.request_router import RequestRouter
from apps.modules.ava.messages.infra.crew_ai.tasks.request_router import (
    RequestRouterTask,
)
from apps.modules.ava.messages.repository_interfaces.ava_messages_repository_interface import (
    IAvaMessagesRepositoryInterface,
)

logger = fastapi_logger.logger


request_router = RequestRouter()
knowledge_researcher = KnowledgeResearcher()

task_router = RequestRouterTask(request_router)


class CreateMessageService:
    """Service for creating messages."""

    def __init__(
        self,
        ava_messages_repository: IAvaMessagesRepositoryInterface,
    ) -> None:
        self.ava_messages_repository = ava_messages_repository

    async def execute(
        self,
        content: str,
    ) -> str:
        """Execute the service to create a message."""

        return await self.ava_messages_repository.create_crew(content)
