from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.modules.ava.messages.controllers.message_request_controller import (
    MessageRequestController,
)
from apps.modules.ava.messages.infra.crew_ai.repositories.ava_messages_repository import (
    AvaMessagesRepository,
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
def get_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    """Get session factory from request state."""

    return request.app.state.db_session_factory


def get_create_message_service(
    session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory),
) -> CreateMessageService:
    """Get create message service."""

    ava_messages_repository = AvaMessagesRepository(session_factory)

    return CreateMessageService(ava_messages_repository)


# Routes
@router.post("/messages")
async def create_ava_message_request(
    body: CreateMessageBodySchema,
    create_message_service: CreateMessageService = Depends(get_create_message_service),
    x_ava_api_key: str = Header(None),
) -> str:
    """Create Ava message."""

    content = body.content

    return await message_request_controller.create(
        content,
        create_message_service,
    )
