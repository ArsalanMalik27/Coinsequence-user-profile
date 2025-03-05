from typing import Type
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.orm import contains_eager

from app.domain.student.data.student_fund_courses import StudentFundCoursesProps
from app.domain.student.repository.db.student_fund_courses import (
    StudentFundCoursesRepository,
)
from app.repository.db.schema.student_fund_courses import StudentFundCourses

# from app.shared.domain.data.page import PageMetadata
from app.shared.repository.db.base import BaseDBRepository


class StudentFundCoursesDBRepository(
    BaseDBRepository[StudentFundCoursesProps, StudentFundCourses],
    StudentFundCoursesRepository
):

    @property
    def _table(self) -> Type[StudentFundCourses]:
        return StudentFundCourses

    @property
    def _entity(self) -> Type[StudentFundCoursesProps]:
        return StudentFundCoursesProps
    
    async def get_by_student_id(self, student_id: UUID) -> list[StudentFundCoursesProps]:
        async with self._db_session() as session:
            query = (
                self.select()
                .where(StudentFundCourses.user_id == student_id)
                .options(contains_eager(self._table.student))
            )
            result = await session.execute(query)
            return list(map(lambda obj: self._entity.from_orm(obj), result.scalars().all()))

    async def delete_all_by_student_id(self, student_id: UUID) -> int:
        async with self._db_session() as session:
            query = (
                delete(self._table)  # type: ignore
                .where((self._table.user_id == student_id))
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount
