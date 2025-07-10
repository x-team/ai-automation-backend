from crewai import Task
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.modules.ava.messages.infra.crew_ai.agents.knowledge_researcher import (
    KnowledgeResearcher,
)
from apps.modules.ava.messages.infra.crew_ai.tools.ava_search_handbook_faq import (
    AvaSearchXteamDocuments,
)


class KnowledgeResearcherTask(Task):
    """Knowledge researcher task."""

    def __init__(
        self,
        agent: KnowledgeResearcher,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        super().__init__(
            description="""
                Use this task to retrieve accurate, up-to-date information from the X-Team Handbook FAQ or X-Team Relevant Links.
                It includes official policies, internal procedures, and details about key people in the company —
                such as their roles, responsibilities, and areas of ownership.
                If the topic involves a person, process, or policy, consider phrasing the question broadly enough to include context or follow-up details.

                Use the user's query to search the Handbook FAQ: {user_query}
            """,
            expected_output="The exact result from the Handbook FAQ or X-Team Relevant Links search, without any rephrasing or summarization. If nothing is found, return a clear note about it.",
            agent=agent,
            tools=[
                AvaSearchXteamDocuments(
                    name="Search Handbook, FAQ or Relevant Links",
                    description="""
                        Retrieves accurate, up-to-date information from the X-Team Handbook, FAQ or relevant links.
                        It includes official policies, internal procedures, and details about key people in the company — such as their roles, responsibilities, and areas of ownership.
                        It also includes links to relevant pages from X-Team.
                    """,
                    session_factory=session_factory,
                ),
            ],
            async_execution=True,
            max_retries=1,
        )
