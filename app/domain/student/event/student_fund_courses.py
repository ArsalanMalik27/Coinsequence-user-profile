from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel


class StudentCourse(BaseModel):
    id: UUID
    user_id: UUID
    college_id: UUID
    course_id: UUID
    college_name: str
    course_name: str

    class Config:
        allow_mutation: True


class StudentFundCourseProps(BaseModel):
    user_id: UUID
    student_courses: list[StudentCourse]

    class Config:
        allow_mutation: True
