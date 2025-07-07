from typing import Any


class AvaMessagesRepository:
    """Repository for Ava messages."""

    def __init__(self, session_factory: Any) -> None:
        self.session_factory = session_factory
