from abc import ABCMeta, abstractmethod
from uuid import UUID
from typing import Any

from app.domain.connections.data.connection import ConnectionProps
from app.shared.domain.data.page import Page, PageMetadata
from app.repository.db.schema.connection import ConnectionConnection
from app.shared.domain.repository.db.base import BaseRepository


class ConnectionRepository(BaseRepository[ConnectionProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def filter_by_profile_id(self, profile_id: UUID) -> Page[ConnectionProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_by_profile_ids(self, profile_a_id: UUID, profile_b_id: int) -> ConnectionProps | None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def create_connection(self, entity: ConnectionProps) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_connection_by_id(self, id: UUID) -> ConnectionProps | None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_connections_by_profile_id(self, profile_id: UUID) -> list[ConnectionProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def count_mutual_connections(self, profile_id: UUID, other_profile_id: UUID) -> int:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_connection_count(self, profile_id: UUID) -> int:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_connected_user(self, user_a: UUID, user_b: UUID) -> int:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def paginate_connection(self, query: Any, page: int = 1, page_size: int = 10) -> tuple[list[ConnectionConnection], PageMetadata]:
        raise NotImplementedError("Subclass should implement this")
