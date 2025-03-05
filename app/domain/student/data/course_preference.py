from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CoursePreference(BaseModel):
    course_id: UUID
    course_start_time: datetime
    course_end_time: datetime
