from abc import ABCMeta, abstractmethod
from uuid import UUID

from app.domain.student.data.student_fund_courses import StudentFundCoursesProps
from app.shared.domain.repository.db.base import BaseRepository


class StudentFundCoursesRepository(BaseRepository[StudentFundCoursesProps]):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_student_id(self, student_id: UUID) -> list[StudentFundCoursesProps]:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def delete_all_by_student_id(self, student_id: UUID) -> int:
        raise NotImplementedError("Subclass should implement this")
