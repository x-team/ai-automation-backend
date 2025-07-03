from crewai import Task

from apps.modules.ava.messages.infra.crew_ai.agents.knowledge_researcher import (
    knowledge_researcher,
)

task_research = Task(
    description="""
        Use this task to retrieve accurate, up-to-date information from the X-Team Handbook FAQ.
        It includes official policies, internal procedures, and details about key people in the company —
        such as their roles, responsibilities, and areas of ownership.
       If the topic involves a person, process, or policy, consider phrasing the question broadly enough to include context or follow-up details.
    """,
    expected_output="The exact result from the Handbook FAQ search, without any rephrasing or summarization. If nothing is found, return a clear note about it.",
    agent=knowledge_researcher,
)
