from typing import AsyncIterable

import redis.asyncio as aioredis
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.application.use_cases.create_embeddings import CreateEmbeddingsUseCase
from app.application.use_cases.create_skills import GetSkillsUseCase
from app.domain.ports.agent.main import AIAgentProtocol
from app.domain.ports.cache.main import CacheProtocol
from app.domain.ports.repository import RepositoryProtocol
from app.domain.ports.uow import AbstractUnitOfWork
from app.infrastructure.adapters.agent.main import AIAgent
from app.infrastructure.adapters.cache.main import Cache
from app.infrastructure.adapters.repository import Repository
from app.infrastructure.adapters.uow import Uow
from app.setup.config import AppSettings, get_app_settings


class ApplicationProvider(Provider):
    """Dependency injection provider for application dependencies."""

    @provide(scope=Scope.APP)
    def provide_app_settings(self) -> AppSettings:
        return get_app_settings()

    @provide(scope=Scope.APP)
    def provide_async_engine(self, settings: AppSettings) -> AsyncEngine:
        return create_async_engine(str(settings.database_url))

    @provide(scope=Scope.APP)
    def provide_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def provide_async_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        session: AsyncSession | None = None
        try:
            session = session_factory()
            yield session
        finally:
            if session and session.is_active:
                await session.close()

    @provide(scope=Scope.REQUEST)
    async def provide_uow(self, session: AsyncSession) -> AbstractUnitOfWork:
        return Uow(session)

    @provide(scope=Scope.REQUEST)
    def provide_aiagent(self, settings: AppSettings) -> AIAgentProtocol:
        return AIAgent(api_key=settings.openai_api_key.get_secret_value())

    @provide(scope=Scope.REQUEST)
    def provide_repository(self, session: AsyncSession) -> RepositoryProtocol:
        return Repository(session=session)

    @provide(scope=Scope.REQUEST)
    async def provide_redis_connection(
        self, settings: AppSettings
    ) -> AsyncIterable[aioredis.Redis]:
        client: aioredis.Redis | None = None
        try:
            client = aioredis.from_url(str(settings.cache_url))
            yield client
        finally:
            if client:
                await client.aclose()

    @provide(scope=Scope.REQUEST)
    def provide_cache(self, redis: aioredis.Redis) -> CacheProtocol:
        return Cache(redis)

    @provide(scope=Scope.REQUEST)
    def provide_get_skills_use_case(
        self,
        aiagent: AIAgentProtocol,
        repository: RepositoryProtocol,
        cache: CacheProtocol,
    ) -> GetSkillsUseCase:
        return GetSkillsUseCase(
            aiagent=aiagent,
            repository=repository,
            cache=cache,
        )

    @provide(scope=Scope.REQUEST)
    def provide_create_embedding_use_case(
        self,
        uow: AbstractUnitOfWork,
        repository: RepositoryProtocol,
        aiagent: AIAgentProtocol,
    ) -> CreateEmbeddingsUseCase:
        return CreateEmbeddingsUseCase(repository=repository, aiagent=aiagent, uow=uow)
