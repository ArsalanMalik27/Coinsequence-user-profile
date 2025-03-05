from typing import Optional, Type
from uuid import UUID

from sqlalchemy import update

from app.domain.student.data.education import EducationProps
from app.domain.student.repository.db.education import EducationRepository
from app.repository.db.schema.education import Education
from app.shared.repository.db.base import BaseDBRepository


class EducationDBRepository(
    BaseDBRepository[EducationProps, Education], EducationRepository
):
    @property
    def _table(self) -> Type[Education]:
        return Education

    @property
    def _entity(self) -> Type[EducationProps]:
        return EducationProps

    async def create_education(self, entity: EducationProps) -> None:
        async with self._db_session() as session:
            query = self._table(**entity.dict(exclude={"address"}))  # type: ignore
            session.add(query)
            await session.commit()

    async def update_education(self, education_props: EducationProps) -> None:
        async with self._db_session() as session:
            entity_dict = education_props.dict(exclude={"address"})
            query = (
                update(self._table)  # type: ignore
                .where(self._table.id == education_props.id)
                .values(**entity_dict)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def delete_education(self, education_id: UUID, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where(
                    (self._table.id == education_id)
                    & (self._table.profile_id == profile_id)
                )
                .values(deleted=True)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def filter_by_profile_id(self, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = self.select().where(self._table.profile_id == profile_id)
            result = await session.execute(query)
            return list(
                map(lambda obj: self._entity.from_orm(obj), result.scalars().all())
            )

    async def update_is_current_by_profile_id(self, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where(
                    (self._table.profile_id == profile_id)
                    & (self._table.is_current == True)
                    & (self._table.deleted != True)
                )
                .values({"is_current": False})
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount
