from abc import ABCMeta, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.student.data.work import WorkProps
from app.shared.domain.repository.db.base import BaseRepository


class WorkRepository(BaseRepository[WorkProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def update_work(self, entity: WorkProps, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def delete_work(self, work_id: UUID, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_all_work(self, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")


