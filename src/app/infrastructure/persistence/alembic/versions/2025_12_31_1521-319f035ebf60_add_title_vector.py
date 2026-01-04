"""Add title_vector

Revision ID: 319f035ebf60
Revises: e16e64bcb50d
Create Date: 2025-12-31 15:21:09.734312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '319f035ebf60'
down_revision: Union[str, None] = 'e16e64bcb50d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('job_post', sa.Column('title_vector', pgvector.sqlalchemy.vector.VECTOR(dim=1536), nullable=True))
    op.create_index(op.f('job_post_title_vector_hnsw'), 'job_post', ['title_vector'], unique=False,
                    postgresql_ops={'title_vector': 'vector_cosine_ops'}, postgresql_using='hnsw')


def downgrade() -> None:
    op.create_index(op.f('job_post_title_vector_hnsw'), 'job_post', ['title_vector'], unique=False,
                    postgresql_ops={'title_vector': 'vector_cosine_ops'}, postgresql_using='hnsw')
    op.drop_column('job_post', 'title_vector')
