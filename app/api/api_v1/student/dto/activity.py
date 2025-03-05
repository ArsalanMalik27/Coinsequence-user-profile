from pydantic import Field
from uuid import UUID, uuid4

from app.domain.student.data.activity import CreateActivityProps, ActivityProps

from app.shared.domain.data.page import PageRequestDTO


class CreateActivityDTO(ActivityProps):
    profile_id: UUID | None = Field(exclude=True)
    pass


class ActivityResponseDTO(ActivityProps):
    profile_id: UUID | None = Field(exclude=True)


class UpdateActivityDTO(CreateActivityProps):
    id : UUID | None
    deleted: bool | None