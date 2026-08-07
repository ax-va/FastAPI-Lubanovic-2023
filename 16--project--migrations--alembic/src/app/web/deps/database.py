from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.sqlalchemy import database as db


# dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a database session for a unit of work and close it afterwards."""
    async with db.async_session_factory() as db_session:
        yield db_session


DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_session),
]
