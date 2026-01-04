import asyncio
import json
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

from app.domain.ports.agent.main import Embedding

semaphore = asyncio.Semaphore(100)

_BASE_DIR = Path(__file__).parent
_PROMPTS_DIR = _BASE_DIR / "prompts"


class AIAgent:
    def __init__(self, api_key: str):
        self._openai = AsyncOpenAI(api_key=api_key)

    async def create_embedding(self, text: str) -> Embedding:
        response = await self._openai.embeddings.create(
            input=text,
            model="text-embedding-3-small",
        )
        return response.data[0].embedding

    async def create_embedding_with_ref(self, item_id: Any, text: str) -> dict[Any, Embedding]:
        response = await self._openai.embeddings.create(
            input=text,
            model="text-embedding-3-small",
        )
        return {item_id: response.data[0].embedding}

    async def extract_skills(self, job_description: str) -> list[str]:
        with open(_PROMPTS_DIR / "extract.txt") as f:
            prompt = f.read()

        async with semaphore:
            response = await self._openai.responses.create(
                model="gpt-4.1-mini",
                temperature=0,
                instructions=prompt,
                input=job_description,
                text={  # type: ignore[invalid-argument-type]
                    "format": {
                        "name": "skills",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "skills": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                }
                            },
                            "required": ["skills"],
                        },
                        "type": "json_schema",
                        "description": "",
                        "strict": False,
                    },
                },
            )

            return json.loads(response.output_text)["skills"]

    async def normalize(self, skills: list[str]) -> list[str]:
        with open(_PROMPTS_DIR / "normalize.txt") as f:
            prompt = f.read()

        response = await self._openai.responses.create(
            model="gpt-4.1-mini",
            temperature=0,
            instructions=prompt,
            input=json.dumps(skills),
            text={  # type: ignore[invalid-argument-type]
                "format": {
                    "name": "skills",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "skills": {
                                "type": "array",
                                "items": {"type": "string"},
                            }
                        },
                        "required": ["skills"],
                    },
                    "type": "json_schema",
                    "description": "",
                    "strict": False,
                },
            },
        )

        return json.loads(response.output_text)["skills"]
