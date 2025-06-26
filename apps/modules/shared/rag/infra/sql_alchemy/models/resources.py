from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from apps.core.infra.sql_alchemy.base import BaseModel

if TYPE_CHECKING:
    from apps.modules.shared.rag.infra.sql_alchemy.models.resource_chunks import (
        ResourceChunkModel,
    )


class ResourceModel(BaseModel):
    """Resource model."""

    __tablename__ = "resources"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    chunks: Mapped[List["ResourceChunkModel"]] = relationship(
        "ResourceChunkModel",
        back_populates="resource",
        lazy="joined",
        cascade="all, delete-orphan",
    )
