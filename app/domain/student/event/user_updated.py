from uuid import UUID

from pydantic import BaseModel


class UserUpdatedData(BaseModel):
    id: UUID
    first_name: str | None
    last_name: str | None

    class Config:
        allow_mutation = False
