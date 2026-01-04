from typing import cast

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import select
from sqlalchemy.orm import defer

from app.domain.dto import JobPost
from app.domain.ports.agent.main import Embedding


class Repository(SQLAlchemyAsyncRepository[JobPost]):  # type: ignore[type-var]
    model_type = JobPost  # type: ignore[type-var]

    async def find_best_matches(self, embedding: Embedding) -> list[JobPost]:
        statement = (
            select(JobPost)
            .options(defer(JobPost.title_vector))  # type: ignore[arg-type]
            .order_by(JobPost.title_vector.op("<=>")(embedding))  # type: ignore[attr-defined]
            .limit(25)
        )
        result = await self.session.execute(statement)
        return cast(list[JobPost], result.scalars().all())
