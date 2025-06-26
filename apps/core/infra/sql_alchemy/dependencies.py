import pkgutil
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


def load_all_models() -> None:
    """Load all models from this folder."""
    modules_dir = Path(__file__).resolve().parent.parent.parent.parent / "modules"
    modules_packages = pkgutil.walk_packages(
        path=[str(modules_dir)],
        prefix="apps.modules",
    )

    # Import models from each module
    for module_package in modules_packages:
        try:
            model_path = f"{module_package.name}.infra.sql_alchemy.models"
            __import__(model_path)
        except ImportError:
            # Skip modules without models
            continue


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:
        yield session
    finally:
        await session.commit()
        await session.close()
