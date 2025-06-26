from datetime import datetime
from typing import List

from pydantic import UUID4, BaseModel


class ResourceChunkBase(BaseModel):
    """Resource chunk base."""

    resource_id: UUID4
    text: str
    chunk_index: int
    embedding: List[float]


class ResourceChunkSearchResponse(BaseModel):
    """Resource chunk search response."""

    resource_name: str
    text: str
    chunk_index: int


class ResourceChunkResponse(ResourceChunkBase):
    """Resource chunk response."""

    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
