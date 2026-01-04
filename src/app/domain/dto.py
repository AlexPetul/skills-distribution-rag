import dataclasses
from dataclasses import asdict, field


@dataclasses.dataclass
class JobPost:
    id: str
    title: str
    description: str
    title_vector: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
