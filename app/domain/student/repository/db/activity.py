from abc import ABCMeta, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.student.data.activity import ActivityProps
from app.shared.domain.repository.db.base import BaseRepository


class ActivityRepository(BaseRepository[ActivityProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def update_activity(self, entity: ActivityProps, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def delete_activity(self, activity_id: UUID, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_all_activities(self, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_by_activity_id(self, profile_id: UUID, activity_id: UUID) -> int:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def bulk_delete(self, profile_id: UUID, entities: list[ActivityProps]) -> None:
        raise NotImplementedError("Subclass should implement this")

