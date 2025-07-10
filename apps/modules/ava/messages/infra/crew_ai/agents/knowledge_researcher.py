from crewai import Agent


class KnowledgeResearcher(Agent):
    """Knowledge researcher agent."""

    def __init__(
        self,
    ) -> None:
        super().__init__(
            role="Internal Knowledge Researcher",
            goal="""
                Find and retrieve accurate, up-to-date information from the X-Team Handbook FAQ or X-Team Relevant Links.
            """,
            backstory="""
                You are a documentation specialist at X-Team. Your obsession is to ensure
                every answer is based on our official knowledge sources.
                You are meticulous, precise, and always prioritize the Handbook.
            """,
            verbose=False,
            allow_delegation=False,
            llm="gpt-4o-mini",
        )
