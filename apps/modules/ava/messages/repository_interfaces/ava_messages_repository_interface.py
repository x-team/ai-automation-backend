from abc import abstractmethod


class IAvaMessagesRepositoryInterface:
    """Interface for Ava messages repository."""

    @abstractmethod
    async def create_crew(self, content: str) -> str:
        """Create a crew."""
