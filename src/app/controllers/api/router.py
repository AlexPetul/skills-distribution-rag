from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from app.application.use_cases.create_embeddings import CreateEmbeddingsUseCase
from app.application.use_cases.create_skills import GetSkillsUseCase

router = APIRouter(route_class=DishkaRoute)


@router.get("/skills")
async def get_skills(
    job_title: str,
    use_case: FromDishka[GetSkillsUseCase],
):
    return await use_case.execute(job_title)


@router.post("/embeddings")
async def embeddings(use_case: FromDishka[CreateEmbeddingsUseCase]):
    await use_case.execute()
