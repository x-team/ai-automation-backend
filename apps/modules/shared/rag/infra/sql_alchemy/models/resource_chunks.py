from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import UUID, ForeignKey, Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from apps.core.infra.sql_alchemy.base import BaseModel

if TYPE_CHECKING:
    from apps.modules.shared.rag.infra.sql_alchemy.models.resources import (
        ResourceModel,
    )

N_DIM = 1536


class ResourceChunkModel(BaseModel):
    """Resource chunk model."""

    __tablename__ = "resource_chunks"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    resource_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resources.id"),
        nullable=False,
    )
    text = mapped_column(String, nullable=False)
    chunk_index = mapped_column(Integer, Identity(start=0), nullable=False)
    embedding = mapped_column(Vector(N_DIM), nullable=False)
    resource: Mapped["ResourceModel"] = relationship(
        "ResourceModel",
        back_populates="chunks",
    )
