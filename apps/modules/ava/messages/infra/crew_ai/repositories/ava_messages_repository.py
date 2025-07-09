from crewai import Crew, Process
from fastapi import logger as fastapi_logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.modules.ava.messages.infra.crew_ai.agents.knowledge_researcher import (
    KnowledgeResearcher,
)
from apps.modules.ava.messages.infra.crew_ai.agents.request_router import RequestRouter
from apps.modules.ava.messages.infra.crew_ai.tasks.knowledge_researcher import (
    KnowledgeResearcherTask,
)
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


class AvaMessagesRepository(IAvaMessagesRepositoryInterface):
    """Repository for Ava messages."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def create_crew(self, content: str) -> str:
        """Create a crew."""

        task_researcher = KnowledgeResearcherTask(
            knowledge_researcher,
            self.session_factory,
        )

        crew = Crew(
            agents=[request_router, knowledge_researcher],
            tasks=[task_router, task_researcher],
            process=Process.sequential,
            verbose=False,
        )

        result = await crew.kickoff_async(
            inputs={
                "user_query": content,
            },
        )

        logger.info(f"Tasks Output: {result.tasks_output}")
        logger.info(f"Token Usage: {result.token_usage}")

        return result.raw
