from dataclasses import dataclass

from src.domain.entities import DiagnosisCode
from src.domain.ports import DiagnosisRepository


@dataclass
class SearchDiagnosisCodes:
    repository: DiagnosisRepository

    def execute(self, term: str | None, limit: int = 50) -> list[DiagnosisCode]:
        return self.repository.search(term=term, limit=limit)
