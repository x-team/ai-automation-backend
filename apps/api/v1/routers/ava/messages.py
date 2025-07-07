from fastapi import APIRouter, Depends

from apps.modules.ava.messages.controllers.message_request_controller import (
    MessageRequestController,
)
from apps.modules.ava.messages.schemas.create_message_body_schema import (
    CreateMessageBodySchema,
)
from apps.modules.ava.messages.services.create_message_service import (
    CreateMessageService,
)

router = APIRouter()

message_request_controller = MessageRequestController()


# Dependency injections
def get_create_message_service() -> CreateMessageService:
    """Get create message service."""

    return CreateMessageService()


# Routes
@router.post("/messages")
async def create_ava_message_request(
    body: CreateMessageBodySchema,
    create_message_service: CreateMessageService = Depends(get_create_message_service),
) -> str:
    """Create Ava message."""

    content = body.content

    return await message_request_controller.create(
        content,
        create_message_service,
    )
