from crewai import Agent


class RequestRouter(Agent):
    """Request router agent."""

    def __init__(self) -> None:
        super().__init__(
            role="Community Request Router",
            goal="""
                Analyze the user's question, identify the main intent (whether it's about general knowledge, a person, or both),
                and route the task to the appropriate specialist.
            """,
            backstory="""
                You are the project manager for the X-Team assistant crew. Your skill is to
                quickly understand what the user needs and delegate the task to the right agent,
                ensuring the work is done as efficiently as possible.
            """,
            tools=[],
            verbose=False,
            allow_delegation=True,
            llm="gpt-4o-mini",
        )
