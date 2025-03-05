from abc import ABCMeta, abstractmethod
from uuid import UUID

from app.domain.student.data.college_universities import CreateUniversityProps
from app.shared.domain.data.page import Page
from app.shared.domain.repository.db.base import BaseRepository


class UniversityRepository(BaseRepository[CreateUniversityProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def update_university(self, entity: CreateUniversityProps, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def delete_university(self, university_id: UUID, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_all_universities(self, profile_id: UUID) -> list:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def universities_count_by_id(self, profile_id: UUID, university_id: UUID) -> int:
        raise NotImplementedError("Subclass should implement this")



