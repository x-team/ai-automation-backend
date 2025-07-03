from crewai import Agent
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from crewai.knowledge.storage.knowledge_storage import KnowledgeStorage

handbook_faq = CSVKnowledgeSource(
    file_paths=[
        "../apps/modules/ava/messages/infra/crew_ai/knowledge/handbook_faq.csv",
    ],
    collection_name="handbook_knowledge",
    storage=KnowledgeStorage(
        collection_name="handbook_knowledge",
    ),
)

knowledge_researcher = Agent(
    role="Internal Knowledge Researcher",
    goal="""
        Find and retrieve accurate, up-to-date information from the X-Team Handbook FAQ.
    """,
    backstory="""
        You are a documentation specialist at X-Team. Your obsession is to ensure
        every answer is based on our official knowledge sources.
        You are meticulous, precise, and always prioritize the Handbook.
    """,
    verbose=True,
    knowledge_sources=[handbook_faq],
    allow_delegation=False,
    llm="gpt-4o-mini",
)
