import asyncio
from multiprocessing import Process, Queue

from crewai.tools import BaseTool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from apps.core.config import settings
from apps.modules.shared.rag.infra.sql_alchemy.repositories.resource_chunks_repository import (
    ResourceChunksRepository,
)
from apps.modules.shared.rag.services.list_resource_chunks import (
    ListResourceChunksService,
)


def search_handbook_faq_process(query: str, queue: "Queue[str]") -> None:
    """Run the search in a separate process."""

    async def _arun(query: str) -> str:
        """Search the Handbook and FAQ for information."""

        engine = create_async_engine(
            str(settings.db_url),
            pool_size=5,
            max_overflow=5,
            pool_recycle=1800,
            pool_pre_ping=True,
        )
        session_factory = async_sessionmaker(engine, expire_on_commit=False)

        async with session_factory() as session:
            resource_chunks_repository = ResourceChunksRepository(session)
            list_resource_chunks_service = ListResourceChunksService(
                resource_chunks_repository,
            )
            vector_search_results = await list_resource_chunks_service.execute(
                query=query,
                chunk_top_k=10,
                resource_names=["handbook_faq.csv"],
            )

        await engine.dispose()

        vector_search = "\n".join([result.text for result in vector_search_results])
        response = settings.openai_client.responses.create(
            model=settings.reasoning_openai_model,
            input=[
                {
                    "role": "system",
                    "content": f"""
                    ## User asked
                    {query}

                    ## Based on the vector search results
                    {vector_search}

                    ## How to answer the user's question:
                    Write a clear, complete, and helpful answer to the user's question. Focus on the most relevant information, but include supporting details from the results if they provide useful context or depth.
                    If multiple entries relate to the same person or topic, group them logically. Do not include information that is unrelated to the user's question or about different topics or people.
                    If the search results include additional context, such as email addresses or URLs that relate to the user's question, make sure to include them in your answer — even if they were not explicitly asked for.
                    Respond in tiny paragraphs form, but make sure the information flows logically and doesn't repeat unnecessarily.
                """,
                },
            ],
        )

        return response.output_text or ""

    result = asyncio.run(_arun(query))
    queue.put(result)


class AvaSearchHandbookFAQ(BaseTool):
    """Search the Handbook and FAQ for information."""

    def _run(self, query: str) -> str:
        """Search the Handbook and FAQ for information."""

        queue: "Queue[str]" = Queue()

        process = Process(target=search_handbook_faq_process, args=(query, queue))
        process.start()

        result = queue.get()
        process.join()

        return result
