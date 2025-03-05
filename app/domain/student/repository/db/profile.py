from abc import ABCMeta, abstractmethod
from typing import Any
from uuid import UUID

from app.api.api_v1.student.dto.search_profile import SearchUsersParams
from app.domain.student.data.profile import UserProfile, UserProfileProps
from app.shared.domain.data.page import Page, PageMetadata
from app.shared.domain.repository.db.base import BaseRepository


class UserProfileRepository(BaseRepository[UserProfileProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> UserProfileProps:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_all_by_user_ids(self, user_ids: list[UUID]) -> Page[UserProfileProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_suggested_users(
        self, user_id: UUID, include_profile_ids: list[UUID], exclude_profile_ids: list[UUID], page: int, page_size: int, text: str
    ) -> Page[UserProfileProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def search_profile_users(
        self,
        user_id: UUID,
        search_user_params: SearchUsersParams,
    ) -> Page[UserProfileProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def update_profile(self, entity: UserProfileProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_profile_by_id(self, id: UUID) -> UserProfileProps:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def create_profile(self, entity: UserProfileProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def paginate_users(self, query: Any, page: int, page_size: int) -> tuple[list[UserProfile], PageMetadata]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_profiles(self, include_profile_ids: list[UUID]) -> list[UserProfileProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_searched_users(
        self,
        page: int,
        page_size: int,
        text: str | None,
        seaarch_user_params: SearchUsersParams
    ) -> Page[UserProfileProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_all_joined_by_user_id(self, id: UUID):
        raise NotImplementedError("Subclass should implement this")
