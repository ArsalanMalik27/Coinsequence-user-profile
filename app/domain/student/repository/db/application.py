from abc import ABCMeta, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.student.data.application import ApplicationProps
from app.shared.domain.repository.db.base import BaseRepository


class ApplicationRepository(BaseRepository[ApplicationProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def filter_by_profile_id(self, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

