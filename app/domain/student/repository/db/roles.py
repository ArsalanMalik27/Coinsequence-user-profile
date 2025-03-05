from abc import ABCMeta, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.student.data.roles import RolesProps
from app.shared.domain.repository.db.base import BaseRepository


class RolesRepository(BaseRepository[RolesProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def create_roles(self, entity: RolesProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def update_roles(self, entity: RolesProps, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def delete_roles(self, roles_id: UUID, profile_id: UUID) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_all_roles(self, profile_id)-> list[RolesProps]:
        raise NotImplementedError("Subclass should implement this")