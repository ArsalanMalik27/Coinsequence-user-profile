from abc import ABCMeta, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.student.data.award import AwardProps
from app.shared.domain.repository.db.base import BaseRepository


class AwardRepository(BaseRepository[AwardProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def update_award(self, entity: AwardProps, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def delete_award(self, award_id: UUID, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_all_awards(self, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")



