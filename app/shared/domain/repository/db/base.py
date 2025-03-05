from abc import ABCMeta, abstractmethod
from typing import Any, Generic, Optional, Type, TypeVar
from uuid import UUID

from app.shared.domain.data.entity import Entity
from app.shared.domain.data.page import PageMetadata

ENTITY_TYPE = TypeVar("ENTITY_TYPE", bound=Entity)


class BaseRepository(Generic[ENTITY_TYPE]):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def _entity(self) -> Type[ENTITY_TYPE]:
        ...

    @abstractmethod
    async def create(self, entity: ENTITY_TYPE) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    def select(self) -> Any:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def paginate(
        self, query: Any, page: int, page_size: int
    ) -> tuple[list[Any], PageMetadata]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def bulk_create(self, entities: list[ENTITY_TYPE]) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[ENTITY_TYPE]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def update(self, entity: ENTITY_TYPE) -> Optional[ENTITY_TYPE]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def delete(self, id: UUID) -> int:
        raise NotImplementedError("Subclass should implement this")
