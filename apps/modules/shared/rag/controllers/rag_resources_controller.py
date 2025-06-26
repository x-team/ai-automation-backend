from apps.modules.shared.rag.services.create_rag_resources import (
    CreateRAGResourcesService,
)


class RAGResourcesController:
    """RAG resources controller."""

    async def create(
        self,
        rag_service: CreateRAGResourcesService,
    ) -> None:
        """Create RAG resources."""

        return await rag_service.execute()

    # def list(self) -> List[T]:
    #     pass

    # def show(self) -> T:
    #     pass

    # def delete(self) -> T:
    #     pass

    # def update(self) -> T:
    #     pass
