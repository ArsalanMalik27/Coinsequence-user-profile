from abc import ABCMeta, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.student.data.voluntary import VoluntaryProps
from app.shared.domain.repository.db.base import BaseRepository


class VoluntaryRepository(BaseRepository[VoluntaryProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def create_voluntary(self, entity: VoluntaryProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def update_voluntary(self, entity: VoluntaryProps, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def delete_voluntary(self, voluntary_id: UUID, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_all_voluntaries(self, profile_id) -> list[VoluntaryProps]:
        raise NotImplementedError("Subclass should implement this")
