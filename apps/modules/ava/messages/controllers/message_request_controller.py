from apps.modules.ava.messages.services.create_message_service import (
    CreateMessageService,
)


class MessageRequestController:
    """Controller for message requests."""

    async def create(
        self,
        content: str,
        create_message_service: CreateMessageService,
    ) -> str:
        """Create a message."""

        return await create_message_service.execute(
            content,
        )
