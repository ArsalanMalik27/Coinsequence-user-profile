from typing import Optional

from pydantic import BaseModel


class Course(BaseModel):
    course_name: str
    institution: str
    course_duration: Optional[int]
