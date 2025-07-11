from crewai.tools import BaseTool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.core.config import settings
from apps.modules.shared.rag.infra.sql_alchemy.repositories.resource_chunks_repository import (
    ResourceChunksRepository,
)
from apps.modules.shared.rag.services.list_resource_chunks import (
    ListResourceChunksService,
)


class AvaSearchXteamDocuments(BaseTool):
    """Search the Handbook, FAQ, and Relevant Links for information."""

    def __init__(
        self,
        name: str,
        description: str,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        super().__init__(
            name=name,
            description=description,
        )
        self._session_factory = session_factory

    async def _run(
        self,
        query: str,
    ) -> str:
        """Search the Handbook, FAQ, and Relevant Links for information."""

        async with self._session_factory() as session:
            resource_chunks_repository = ResourceChunksRepository(session)
            list_resource_chunks_service = ListResourceChunksService(
                resource_chunks_repository,
            )
            vector_search_results = await list_resource_chunks_service.execute(
                query=query,
                chunk_top_k=10,
                resource_names=["ava_relevant_links.csv", "handbook_faq.csv"],
            )

            vector_search = "\n".join(
                [result.text for result in vector_search_results],
            )

            response = await settings.openai_client_async.responses.create(
                model=settings.base_openai_model,
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
