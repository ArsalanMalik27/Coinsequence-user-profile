from abc import ABCMeta, abstractmethod
from uuid import UUID

from app.domain.connections.data.connection_request import (
    ConnectionRequestProps,
    ConnectionRequestStatus,
)
from app.shared.domain.repository.db.base import BaseRepository


class ConnectionRequestRepository(BaseRepository[ConnectionRequestProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def filter_by_receiver_id(self, receiver_id: UUID, status: ConnectionRequestStatus | None, page: int, page_size: int) -> ConnectionRequestProps | None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_by_profile_ids(self, profile_a_id: UUID, profile_b_id: int, status: ConnectionRequestStatus | None) -> ConnectionRequestProps | None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_pending_by_id(self, id: UUID) -> ConnectionRequestProps | None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def create_connection_request(self, entity: ConnectionRequestProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def update_connection_request(self, entity: ConnectionRequestProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def filter_by_profile_id(self, profile_id: UUID, status: ConnectionRequestStatus | None, page: int, page_size: int, text: str) -> ConnectionRequestProps | None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_pending_connection_request_count(self, profile_id: UUID)-> int:
        raise NotImplementedError("Subclass should implement this")
