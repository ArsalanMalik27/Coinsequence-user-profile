from typing import Type
from uuid import UUID

from sqlalchemy import and_, func, update

from app.domain.student.data.activity import ActivityProps
from app.domain.student.repository.db.activity import ActivityRepository
from app.repository.db.schema.activity import Activity
from app.shared.repository.db.base import BaseDBRepository


class ActivityDBRepository(
    BaseDBRepository[ActivityProps, Activity], ActivityRepository
):
    @property
    def _table(self) -> Type[Activity]:
        return Activity

    @property
    def _entity(self) -> Type[ActivityProps]:
        return ActivityProps

    async def update_activity(self, entity: ActivityProps, profile_id: UUID) -> None:
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

    async def delete_activity(self, activity_id: UUID, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where(
                    (self._table.id == activity_id)
                    & (self._table.profile_id == profile_id)
                )
                .values(deleted=True)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def get_all_activities(self, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                self.select()
                .where(
                    (self._table.profile_id == profile_id)
                    & (self._table.deleted != True)
                )
                .execution_options(synchronize_session="fetch")
            )
            results = await session.execute(query)
            return list(
                map(lambda obj: self._entity.from_orm(obj), results.scalars().all())
            )

    async def get_by_activity_id_count(
        self, profile_id: UUID, activity_id: UUID
    ) -> int:
        async with self._db_session() as session:
            query = (
                self.select()
                .where(
                    (self._table.profile_id == profile_id)
                    & (self._table.activity_id == activity_id)
                )
                .execution_options(synchronize_session="fetch")
            )
            counter = query.with_only_columns(func.count())
            results = await session.execute(counter)
            count = results.scalar()
            return count

    async def bulk_delete(
        self, profile_id: UUID, entities: list[ActivityProps]
    ) -> None:
        async with self._db_session() as session:
            ids = [entity.id for entity in entities]
            query = (
                update(self._table)  # type: ignore
                .where(
                    and_(self._table.profile_id == profile_id, self._table.id.in_(ids))
                )
                .values(deleted=True)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount
