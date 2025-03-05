from abc import abstractmethod
from typing import Any, Generic, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.shared.domain.data.entity import Entity
from app.shared.domain.data.page import PageMetadata
from app.shared.domain.repository.db.base import BaseRepository
from app.shared.repository.db.schema.base import BaseTableMixin
from app.shared.utils.error import DomainError

ENTITY_TYPE = TypeVar("ENTITY_TYPE", bound=Entity)
TABLE_TYPE = TypeVar("TABLE_TYPE", bound=BaseTableMixin)


class BaseDBRepository(Generic[ENTITY_TYPE, TABLE_TYPE], BaseRepository[ENTITY_TYPE]):
    @property
    @abstractmethod
    def _table(self) -> Type[TABLE_TYPE]:
        ...

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    def select(self) -> Any:
        return select(self._table).where(self._table.deleted == False)

    async def paginate(
        self, query: Any, page: int, page_size: int
    ) -> tuple[list[TABLE_TYPE], PageMetadata]:
        async with self._db_session() as session:
            if page <= 0:
                raise DomainError("page should be be >= 1")
            if page_size <= 0:
                raise DomainError("page_size should be >= 1")
            paginated_query = query.limit(page_size).offset((page - 1) * page_size)
            count_query = query.with_only_columns(func.count(self._table.id))
            results = await session.execute(paginated_query)
            total_result = await session.execute(count_query)
            page_data = PageMetadata(
                page=page,
                page_size=page_size,
                total=total_result.scalar_one(),
            )
            return (results.scalars().unique().all(), page_data)

    async def create(self, entity: ENTITY_TYPE) -> None:
        async with self._db_session() as session:
            query = self._table(**entity.dict())
            session.add(query)
            await session.commit()

    async def bulk_create(self, entities: list[ENTITY_TYPE]) -> None:
        async with self._db_session() as session:
            objects = []
            for entity in entities:
                objects.append(self._table(**entity.dict()))
            session.add_all(objects)
            await session.commit()

    async def get_by_id(self, id: UUID) -> Optional[ENTITY_TYPE]:
        async with self._db_session() as session:
            query = self.select().where(self._table.id == id)
            results = await session.execute(query)
            record = results.scalars().one_or_none()
            if not record:
                return None
            return self._entity.from_orm(record)

    async def update(self, entity: ENTITY_TYPE) -> None:
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where(self._table.id == entity.id)
                .values(**entity.dict())
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()

    async def create_or_update(self, entity: ENTITY_TYPE) -> None:
        async with self._db_session() as session:
            session.merge(self._table(**entity.dict()))
            await session.commit()

    async def delete(self, id: UUID) -> int:
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where(self._table.id == id)
                .values(deleted=True)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount
