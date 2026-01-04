import asyncio
import logging
from typing import Any, TypeAlias, Union

from advanced_alchemy.filters import LimitOffset

from app.domain.dto import JobPost
from app.domain.ports.agent.main import AIAgentProtocol, Embedding
from app.domain.ports.repository import RepositoryProtocol
from app.domain.ports.uow import AbstractUnitOfWork

TaskResult: TypeAlias = Union[BaseException, dict[Any, Embedding]]


class CreateEmbeddingsUseCase:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        repository: RepositoryProtocol,
        aiagent: AIAgentProtocol,
    ):
        self._uow = uow
        self._repository = repository
        self._aiagent = aiagent

    async def execute(self):
        offset, chunk_size = 0, 500

        while True:
            rows = await self._repository.list(
                LimitOffset(limit=chunk_size, offset=offset),
                JobPost.title_vector.is_(None),  # type: ignore
            )
            if not rows:
                break

            rows = {row.id: row for row in rows}

            tasks = [
                self._aiagent.create_embedding_with_ref(job_post_id, job_post.title)
                for job_post_id, job_post in rows.items()
            ]
            task_results: list[TaskResult] = await asyncio.gather(*tasks, return_exceptions=True)

            result = {}
            for task_result in task_results:
                if isinstance(task_result, BaseException):
                    logging.warning("Task failed with exception %s", task_result)
                else:
                    result.update(task_result)

            for job_post_id, embedding in result.items():
                rows[job_post_id].title_vector = embedding

            async with self._uow:
                await self._repository.update_many(list(rows.values()))

            offset += chunk_size
