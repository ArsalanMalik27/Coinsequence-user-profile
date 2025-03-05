from typing import Type
from uuid import UUID

from sqlalchemy import update

from app.domain.student.data.work import WorkProps
from app.domain.student.repository.db.work import WorkRepository
from app.repository.db.schema.work import Work
from app.shared.repository.db.base import BaseDBRepository


class WorkDBRepository(BaseDBRepository[WorkProps, Work], WorkRepository):
    @property
    def _table(self) -> Type[Work]:
        return Work

    @property
    def _entity(self) -> Type[WorkProps]:
        return WorkProps

    async def update_work(self, entity: WorkProps, profile_id: UUID) -> None:
        async with self._db_session() as session:
            entity_dict = entity.dict()
            query = (
                update(self._table)  # type: ignore
                .where(
                    (self._table.id == entity.id)
                    & (self._table.profile_id == profile_id)
                )
                .values(**entity_dict)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def delete_work(self, work_id: UUID, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where(
                    (self._table.id == work_id) & (self._table.profile_id == profile_id)
                )
                .values(deleted=True)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def get_all_work(self, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                self.select()
                .where(self._table.profile_id == profile_id)
                .execution_options(synchronize_session="fetch")
            )
            results = await session.execute(query)
            return list(
                map(lambda obj: self._entity.from_orm(obj), results.scalars().all())
            )
