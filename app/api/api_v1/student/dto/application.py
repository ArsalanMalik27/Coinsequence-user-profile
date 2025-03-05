from pydantic import Field
from uuid import UUID, uuid4

from app.domain.student.data.application import CreateApplicationProps, ApplicationProps
from app.shared.domain.data.page import PageRequestDTO


class CreateApplicationDTO(CreateApplicationProps):
    pass


class ApplicationResponseDTO(ApplicationProps):
    pass
