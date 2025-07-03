from crewai import Crew, Process
from fastapi import logger as fastapi_logger

from apps.modules.ava.messages.infra.crew_ai.agents.knowledge_researcher import (
    knowledge_researcher,
)
from apps.modules.ava.messages.infra.crew_ai.agents.request_router import request_router
from apps.modules.ava.messages.infra.crew_ai.tasks.knowledge_researcher import (
    task_research,
)
from apps.modules.ava.messages.infra.crew_ai.tasks.request_router import task_route

logger = fastapi_logger.logger


class CreateMessageService:
    """Service for creating messages."""

    def __init__(self) -> None:
        pass

    async def execute(self, content: str) -> str:
        """Execute the service to create a message."""

        crew = Crew(
            agents=[request_router, knowledge_researcher],
            tasks=[task_route, task_research],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff(
            inputs={
                "user_query": content,
            },
        )

        logger.info(f"Tasks Output: {result.tasks_output}")
        logger.info(f"Token Usage: {result.token_usage}")

        return result.raw
