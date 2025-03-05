from pydantic import Field
from uuid import UUID, uuid4

from app.domain.student.data.roles import CreateRolesProps, RolesProps

from app.shared.domain.data.page import PageRequestDTO


class CreateRolesDTO(CreateRolesProps):
    pass


class UpdateRolesDTO(CreateRolesProps):
    pass


class RolesResponseDTO(RolesProps):
    profile_id: UUID | None = Field(exclude=True)
