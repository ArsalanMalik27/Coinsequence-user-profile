from uuid import UUID

from pydantic import Field

from app.domain.student.data.education import CreateEducationProps, EducationProps
from app.shared.domain.data.page import PageRequestDTO


class CreateEducationDTO(CreateEducationProps):
    pass


class UpdateEducationDTO(CreateEducationProps):
    pass


class EducationResponseDTO(EducationProps):
    profile_id: UUID | None = Field(exclude=True)
    address_id: UUID | None = Field(exclude=True)

class EducationParams(PageRequestDTO):
    pass