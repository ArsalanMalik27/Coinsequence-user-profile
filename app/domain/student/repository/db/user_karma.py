from abc import ABCMeta, abstractmethod
from uuid import UUID

from app.domain.student.data.user_karma import UserKarmaProps
from app.shared.domain.repository.db.base import BaseRepository


class UserKarmaRepository(BaseRepository[UserKarmaProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_user_id(self, entity: UserKarmaProps, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_by_tag_id_and_user_id(self, user_id: UUID, tag_id: UUID) -> UserKarmaProps | None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def create_user_karma(self, entity: UserKarmaProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def update_user_karma(self, entity: UserKarmaProps, user_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")