from abc import ABCMeta, abstractmethod
from uuid import UUID

from app.domain.student.data.children_profile import ChildrenProfileProps
from app.shared.domain.data.page import Page
from app.shared.domain.repository.db.base import BaseRepository
from app.domain.student.data.profile import UserProfile


class ChildrenProfileRepository(BaseRepository[ChildrenProfileProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def filter_by_parent_id(self,parent_id: UUID) -> list[ChildrenProfileProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def count_children_by_child_id(self, child_id: UUID) -> int:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_by_profile_ids(self, child_id: UUID, parent_id: UUID) -> ChildrenProfileProps:
        raise NotImplementedError("Subclass should implement this")







