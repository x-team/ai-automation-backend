from datetime import datetime
from typing import List

from pydantic import UUID4, BaseModel

from apps.modules.shared.rag.schemas.resource_chunk_schema import ResourceChunkResponse


class ResourceBase(BaseModel):
    """Message base."""

    name: str
    content: str


class ResourceResponse(ResourceBase):
    """Resource response."""

    id: UUID4
    chunks: List[ResourceChunkResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
