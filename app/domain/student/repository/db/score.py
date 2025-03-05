from abc import ABCMeta, abstractmethod
from uuid import UUID
from typing import Optional, List
from app.shared.domain.repository.db.base import BaseRepository
from app.domain.student.data.score import ScoreProps


class ScoreRepository(BaseRepository[ScoreProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def update_score(self, entity: ScoreProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_data_by_score_id(self, score_id: UUID) -> Optional[ScoreProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_score_list(self, profile_id: UUID) -> List:
        raise NotImplementedError("Subclass should implement this")
