from crewai import Task

from apps.modules.ava.messages.infra.crew_ai.agents.knowledge_researcher import (
    KnowledgeResearcher,
)
from apps.modules.ava.messages.infra.crew_ai.tools.ava_search_handbook_faq import (
    AvaSearchHandbookFAQ,
)


class KnowledgeResearcherTask(Task):
    """Knowledge researcher task."""

    def __init__(
        self,
        agent: KnowledgeResearcher,
    ) -> None:
        super().__init__(
            description="""
                Use this task to retrieve accurate, up-to-date information from the X-Team Handbook FAQ.
                It includes official policies, internal procedures, and details about key people in the company —
                such as their roles, responsibilities, and areas of ownership.
                If the topic involves a person, process, or policy, consider phrasing the question broadly enough to include context or follow-up details.

                Use the user's query to search the Handbook FAQ: {user_query}
            """,
            expected_output="The exact result from the Handbook FAQ search, without any rephrasing or summarization. If nothing is found, return a clear note about it.",
            agent=agent,
            tools=[
                AvaSearchHandbookFAQ(
                    name="Search Handbook FAQ",
                    description="Retrieves accurate, up-to-date information from the X-Team Handbook FAQ. It includes official policies, internal procedures, and details about key people in the company — such as their roles, responsibilities, and areas of ownership.",
                ),
            ],
            async_execution=True,
            max_retries=1,
        )
