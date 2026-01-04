from typing import Protocol, runtime_checkable

from advanced_alchemy.repository import SQLAlchemyAsyncRepositoryProtocol

from app.domain.dto import JobPost
from app.domain.ports.agent.main import Embedding


@runtime_checkable
class RepositoryProtocol(SQLAlchemyAsyncRepositoryProtocol[JobPost], Protocol):  # type: ignore[type-var]
    """Extended SQLAlchemy repository protocol."""

    async def find_best_matches(self, embedding: Embedding) -> list[JobPost]:
        """Return job IDs ranked by relevance to the query."""
