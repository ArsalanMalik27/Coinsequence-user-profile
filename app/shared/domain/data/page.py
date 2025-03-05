from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel

from app.shared.domain.data.entity import Entity

ENTITY_TYPE = TypeVar("ENTITY_TYPE", bound=Entity)


class PageRequestDTO(BaseModel):
    page: int = Query(default=1, title="page")
    page_size: int = Query(default=10, le=200, title="page_size")


class PageMetadata(BaseModel):
    page: int
    page_size: int
    total: int

    class Config:
        allow_mutation = False
        orm_mode = True


class Page(Generic[ENTITY_TYPE], PageMetadata):
    items: list[ENTITY_TYPE]
