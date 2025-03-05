from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Entity(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted: bool | None

    class Config:
        allow_mutation = False

    def delete(self):
        self.deleted = True
        self.updated_at = datetime.now()
