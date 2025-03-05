from typing import Type
from uuid import UUID

from sqlalchemy import update

from app.domain.student.data.voluntary import VoluntaryProps
from app.domain.student.repository.db.voluntary import VoluntaryRepository
from app.repository.db.schema.voluntary import Voluntary
from app.shared.domain.data.page import Page, PageMetadata
from app.shared.repository.db.base import BaseDBRepository


class VoluntaryDBRepository(
    BaseDBRepository[VoluntaryProps, Voluntary], VoluntaryRepository
):
    @property
    def _table(self) -> Type[Voluntary]:
        return Voluntary

    @property
    def _entity(self) -> Type[VoluntaryProps]:
        return VoluntaryProps

    async def create_voluntary(self, entity: VoluntaryProps) -> None:
        async with self._db_session() as session:
            query = self._table(**entity.dict())  # type: ignore
            session.add(query)
            await session.commit()

    async def update_voluntary(self, entity: VoluntaryProps, profile_id: UUID) -> None:
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

    async def delete_voluntary(self, voluntary_id: UUID, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where(
                    (self._table.id == voluntary_id)
                    & (self._table.profile_id == profile_id)
                )
                .values(deleted=True)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def get_all_voluntaries(self, profile_id) -> list[VoluntaryProps]:
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
