from pydantic import Field
from uuid import UUID, uuid4

from app.domain.student.data.award import CreateAwardProps, AwardProps

from app.shared.domain.data.page import PageRequestDTO


class CreateAwardDTO(CreateAwardProps):
    pass


class AwardResponseDTO(AwardProps):
    profile_id: UUID | None = Field(exclude=True)


class UpdateAwardDTO(CreateAwardProps):
    pass