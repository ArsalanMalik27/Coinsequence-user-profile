from typing import List, Optional, Type
from uuid import UUID

from sqlalchemy import func, update

from app.domain.student.data.grade import GradeProps
from app.domain.student.repository.db.grade import GradeRepository
from app.repository.db.schema.grade import Grade
from app.shared.domain.data.page import Page
from app.shared.repository.db.base import BaseDBRepository


class GradeDBRepository(BaseDBRepository[GradeProps, Grade], GradeRepository):
    @property
    def _table(self) -> Type[Grade]:
        return Grade

    @property
    def _entity(self) -> Type[GradeProps]:
        return GradeProps

    async def update_grade(self, entity: GradeProps):
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where((self._table.id == entity.id))
                .values(**entity.dict())
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def grade_list(self, profile_id: UUID) -> Optional[List[GradeProps]]:
        async with self._db_session() as session:
            query = self.select().where(
                (self._table.profile_id == profile_id) & (self._table.deleted != True)
            )
            results = await session.execute(query)
            return list(
                map(lambda obj: self._entity.from_orm(obj), results.scalars().all())
            )

    async def grade_count_by_level(self, profile_id: UUID, level: str) -> int:
        async with self._db_session() as session:
            query = self.select().where(
                (self._table.profile_id == profile_id) & (self._table.level == level)
            )
            counter = query.with_only_columns(func.count())
            results = await session.execute(counter)
            count = results.scalar()
            return count
