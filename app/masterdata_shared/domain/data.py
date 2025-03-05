from app.shared.domain.data.entity import Entity
from typing import  Optional


class TestProps(Entity):
    name: str
    is_free_text_subject: bool | None
    min: int
    max: int
    step: int = 10


    class Config:
        allow_mutation = True
        orm_mode = True

class CourseProps(Entity):
    fees: int
    name : str
    duration: int
    url: str


    class Config:
        allow_mutation = True
        orm_mode = True