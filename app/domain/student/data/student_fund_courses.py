from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.student.event.student_fund_courses import (
    StudentCourse as StudentCourseEvent,
)
from app.shared.domain.data.entity import Entity


class StudentFundCoursesProps(Entity):
    user_id: UUID
    college_id: UUID | None
    course_id: UUID | None
    college_name: str | None
    course_name: str | None

    class Config:
        allow_mutation = True
        orm_mode = True


@dataclass
class StudentFundCourses:
    props: StudentFundCoursesProps

    @staticmethod
    def from_event(user_id: UUID, student_course: StudentCourseEvent):
        time_now = datetime.now()
        props = StudentFundCoursesProps(
            id=student_course.id,
            created_at=time_now,
            updated_at=time_now,
            user_id=user_id,
            college_id=student_course.college_id,
            college_name=student_course.college_name,
            course_id=student_course.course_id,
            course_name=student_course.course_name,
        )
        return StudentFundCourses(props=props)

