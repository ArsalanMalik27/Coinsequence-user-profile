from abc import ABCMeta, abstractmethod
from uuid import UUID

from app.domain.student.data.profile_privacy import ProfilePrivacyProps
from app.shared.domain.data.page import Page
from app.shared.domain.repository.db.base import BaseRepository


class ProfilePrivacyRepository(BaseRepository[ProfilePrivacyProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def filter(self, profile_id: UUID) -> list[ProfilePrivacyProps]:
        raise NotImplementedError("Subclass should implement this")
