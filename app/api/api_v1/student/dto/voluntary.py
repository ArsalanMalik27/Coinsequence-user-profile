from pydantic import Field
from uuid import UUID, uuid4

from app.domain.student.data.voluntary import CreateVoluntaryProps, VoluntaryProps

from app.shared.domain.data.page import PageRequestDTO


class CreateVoluntaryDTO(CreateVoluntaryProps):
    pass


class UpdateVoluntaryDTO(CreateVoluntaryProps):
    pass


class VoluntaryResponseDTO(VoluntaryProps):
    profile_id: UUID | None = Field(exclude=True)
