from fastapi import Query
from pydantic import Field

from app.shared.domain.data.page import PageRequestDTO


class SearchUsersQuery(PageRequestDTO):
    query: str = Query(default="", title="query")


class SearchUsersParams(PageRequestDTO):
    ACADEMIC: list[str] = Field(Query([]))
    ARTS: list[str] = Field(Query([]))
    ATTRIBUTES: list[str] = Field(Query([]))
    COLLEGE: list[str] = Field(Query([]))
    COLLEGE_COURSE: list[str] = Field(Query([]))
    EHTINICITY: list[str] = Field(Query([]))
    GRADES: list[str] = Field(Query([]))
    HOBBIES: list[str] = Field(Query([]))
    SCHOOL: list[str] = Field(Query([]))
    SCORE: list[str] = Field(Query([]))
    SOCIETIES: list[str] = Field(Query([]))
    SPORTS: list[str] = Field(Query([]))
    VOLUNTEERING: list[str] = Field(Query([]))
    WELLBEING: list[str] = Field(Query([]))
