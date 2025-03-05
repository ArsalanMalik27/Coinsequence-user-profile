from typing import Type
from uuid import UUID

from sqlalchemy import update

from app.domain.student.data.award import AwardProps
from app.domain.student.repository.db.award import AwardRepository
from app.repository.db.schema.award import Award
from app.shared.repository.db.base import BaseDBRepository


class AwardDBRepository(BaseDBRepository[AwardProps, Award], AwardRepository):
    @property
    def _table(self) -> Type[Award]:
        return Award

    @property
    def _entity(self) -> Type[AwardProps]:
        return AwardProps

    async def update_award(self, entity: AwardProps, profile_id: UUID) -> None:
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

    async def delete_award(self, award_id: UUID, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where(
                    (self._table.id == award_id)
                    & (self._table.profile_id == profile_id)
                )
                .values(deleted=True)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def get_all_awards(self, profile_id: UUID) -> None:
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
