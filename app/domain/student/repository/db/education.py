from abc import ABCMeta, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.student.data.education import EducationProps
from app.shared.domain.repository.db.base import BaseRepository


class EducationRepository(BaseRepository[EducationProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def create_education(self, entity: EducationProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def update_education(self, education_props: EducationProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def filter_by_profile_id(self, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def delete_education(self,education_id: UUID, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def update_is_current_by_profile_id(self, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")
