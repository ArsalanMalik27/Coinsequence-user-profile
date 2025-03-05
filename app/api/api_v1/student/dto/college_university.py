from pydantic import Field
from uuid import UUID, uuid4

from app.domain.student.data.college_universities import CreateUniversityProps, UniversityProps


class CreateUniversityDTO(UniversityProps):
    pass


class UpdateUniversityDTO(UniversityProps):
    pass


class UniversityResponseDTO(CreateUniversityProps):
    pass

