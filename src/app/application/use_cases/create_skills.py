import asyncio
import itertools
import json
from collections import Counter
from typing import TypeAlias

from app.domain.ports.agent.main import AIAgentProtocol
from app.domain.ports.cache.main import CacheProtocol
from app.domain.ports.repository import RepositoryProtocol

SkillsMap: TypeAlias = dict[str, int]


class GetSkillsUseCase:
    """UseCase for getting skills for a given job title."""

    def __init__(
        self,
        repository: RepositoryProtocol,
        aiagent: AIAgentProtocol,
        cache: CacheProtocol,
    ):
        self._repository = repository
        self._aiagent = aiagent
        self._cache = cache

    async def execute(self, job_title: str) -> SkillsMap:
        if cached_result := await self._cache.get(job_title):
            return json.loads(cached_result)

        embedding = await self._aiagent.create_embedding(job_title)

        job_posts = await self._repository.find_best_matches(embedding)

        tasks = [self._aiagent.extract_skills(job_post.description) for job_post in job_posts]
        results: list[list[str]] = await asyncio.gather(*tasks)

        skills = list(itertools.chain(*results))

        skills = await self._aiagent.normalize(skills)
        counter = Counter(skills)
        counter_sorted = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
        result = dict(itertools.islice(counter_sorted.items(), 15))
        await self._cache.set(job_title, json.dumps(result))
        return result
