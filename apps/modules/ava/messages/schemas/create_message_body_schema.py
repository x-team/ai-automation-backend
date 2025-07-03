from pydantic import BaseModel


class CreateMessageBodySchema(BaseModel):
    """Schema for creating a message."""

    content: str
