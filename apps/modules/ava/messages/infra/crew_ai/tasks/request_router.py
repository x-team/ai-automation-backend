from crewai import Task

from apps.modules.ava.messages.infra.crew_ai.agents.request_router import RequestRouter


class RequestRouterTask(Task):
    """Request router task."""

    def __init__(self, agent: RequestRouter) -> None:
        super().__init__(
            description="""
                Analyze the following user query: '{user_query}'.
                Determine if the main intent is to get knowledge from the Handbook
                or information about a user profile. Provide a clear summary of the intent.
            """,
            expected_output="A summary of the user's intent and which specialist (KnowledgeResearcher or PeopleExpert) should be engaged.",
            agent=agent,
        )
