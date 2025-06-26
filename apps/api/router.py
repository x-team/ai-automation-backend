from fastapi.routing import APIRouter

from apps.api.v1.routers import docs, monitor, rag
from apps.api.v1.routers.quinn import slides

api_router = APIRouter()

## v1 Routers

# Shared
api_router.include_router(monitor.router, prefix="/v1", tags=["Monitor"])
api_router.include_router(rag.router, prefix="/v1", tags=["RAG"])
api_router.include_router(docs.router, prefix="/v1")

# Quinn Routers
api_router.include_router(slides.router, prefix="/v1/quinn", tags=["Quinn"])
