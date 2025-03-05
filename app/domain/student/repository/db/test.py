from abc import ABCMeta, abstractmethod
from uuid import UUID
from typing import Optional, List
from app.shared.domain.repository.db.base import BaseRepository
from app.domain.student.data.test import TestProps


class TestRepository(BaseRepository[TestProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def update_test(self, entity: TestProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_by_test_id(self, test_id: UUID) -> Optional[TestProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_test_list_by_profile_id(self, profile_id: UUID) -> List:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def create_test(self, entity: TestProps) -> None:
        raise NotImplementedError("Subclass should implement this")
