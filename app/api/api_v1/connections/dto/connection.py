from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.shared.domain.data.page import PageRequestDTO


class ConnectionResponseDTO(BaseModel):
    profile: UUID
    created_at: datetime


class ConnectionsParams(PageRequestDTO):
    pass
