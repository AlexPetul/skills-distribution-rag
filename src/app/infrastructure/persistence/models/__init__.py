from sqlalchemy import inspect

from app.domain.dto import JobPost
from app.infrastructure.persistence.models.job_post import map_job_post_table


def map_all_tables():
    if not inspect(JobPost, raiseerr=False):
        map_job_post_table()
