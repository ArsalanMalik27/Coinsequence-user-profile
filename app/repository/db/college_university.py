from typing import Any, Optional, Type
from uuid import UUID

from sqlalchemy import and_, func, update
from sqlalchemy.orm import contains_eager

from app.domain.student.data.college_universities import CreateUniversityProps
from app.domain.student.repository.db.college_university import UniversityRepository
from app.repository.db.schema.college_universities import CollegeUniversities
from app.shared.domain.data.page import Page, PageMetadata
from app.shared.repository.db.base import BaseDBRepository


class UniversityDBRepository(
    BaseDBRepository[CreateUniversityProps, CollegeUniversities], UniversityRepository
):
    @property
    def _table(self) -> Type[CollegeUniversities]:
        return CollegeUniversities

    @property
    def _entity(self) -> Type[CreateUniversityProps]:
        return CreateUniversityProps

    async def update_university(
        self, entity: CreateUniversityProps, profile_id: UUID
    ) -> None:
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
            await session.execute(query)
            await session.commit()

    async def delete_university(self, university_id: UUID, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where(
                    (self._table.id == university_id)
                    & (self._table.profile_id == profile_id)
                )
                .values(deleted=True)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def get_all_universities(self, profile_id: UUID) -> list:
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

    async def universities_count_by_id(
        self, profile_id: UUID, university_id: UUID
    ) -> int:
        async with self._db_session() as session:
            query = self.select().where(
                (self._table.profile_id == profile_id)
                & (self._table.university_id == university_id)
            )
            counter = query.with_only_columns(func.count())
            results = await session.execute(counter)
            count = results.scalar()
            return count
