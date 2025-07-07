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

logger = fastapi_logger.logger


request_router = RequestRouter()
knowledge_researcher = KnowledgeResearcher()

task_router = RequestRouterTask(request_router)


class CreateMessageService:
    """Service for creating messages."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def execute(
        self,
        content: str,
    ) -> str:
        """Execute the service to create a message."""

        task_researcher = KnowledgeResearcherTask(
            knowledge_researcher,
            self._session_factory,
        )

        # TODO: move this to a repository
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
