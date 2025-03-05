from pydantic import Field
from uuid import UUID, uuid4

from app.domain.student.data.work import CreateWorkProps, WorkProps


class CreateWorkDTO(CreateWorkProps):
    pass


class WorkResponseDTO(WorkProps):
    profile_id: UUID | None = Field(exclude=True)


class UpdateWorkDTO(CreateWorkProps):
    pass