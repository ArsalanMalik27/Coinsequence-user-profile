from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel


class DomainEvent(BaseModel):
    name: str
    data: BaseModel
    created_at: datetime = datetime.now()
    id: UUID = uuid4()
    occurred_on: Optional[datetime] = None

    class Config:
        allow_mutation = False
        orm_mode = True
