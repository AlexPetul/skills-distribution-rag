from typing import Any, Protocol, TypeAlias

_Ref: TypeAlias = Any
Embedding: TypeAlias = list[float]


class AIAgentProtocol(Protocol):
    async def create_embedding(self, text: str) -> Embedding: ...

    async def create_embedding_with_ref(self, item_id: _Ref, text: str) -> dict[_Ref, Embedding]:
        """Create embedding with reference."""

    async def extract_skills(self, job_description: str) -> list[str]: ...

    async def normalize(self, skills: list[str]) -> list[str]:
        """Perform normalization on a list of skills.

        - replace the abbreviated form with the full one
        - combine similar entries into one, etc.
        """
