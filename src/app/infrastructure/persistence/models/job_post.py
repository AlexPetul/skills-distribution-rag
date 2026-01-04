from pgvector.sqlalchemy import Vector  # type: ignore[import-untyped]
from sqlalchemy import UUID, Column, String, Table, Text

from app.domain.dto import JobPost
from app.infrastructure.persistence.registry import mapper_registry, metadata

job_post_table = Table(
    "job_post",
    metadata,
    Column("id", UUID(as_uuid=False), primary_key=True),
    Column("title", String(255), nullable=False),
    Column("title_vector", Vector(1536)),
    Column("description", Text, nullable=False),
)


def map_job_post_table() -> None:
    mapper_registry.map_imperatively(
        JobPost,
        job_post_table,
    )
