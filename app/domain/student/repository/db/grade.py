from abc import ABCMeta, abstractmethod
from typing import Optional, List
from uuid import UUID

from app.domain.student.data.grade import GradeProps
from app.shared.domain.repository.db.base import BaseRepository


class GradeRepository(BaseRepository[GradeProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def update_grade(self, entity: GradeProps) -> Optional[GradeProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def grade_list(self, profile_id: UUID) -> Optional[List[GradeProps]]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def grade_count_by_level(self, profile_id: UUID, level: str) -> int:
        raise NotImplementedError("Subclass should implement this")
