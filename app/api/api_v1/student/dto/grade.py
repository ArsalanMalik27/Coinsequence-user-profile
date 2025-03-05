from app.domain.student.data.grade import CreateGradeProps, GradeProps
from app.shared.domain.data.page import PageRequestDTO


class CreateGradeDTO(CreateGradeProps):
    pass


class UpdateGradeDTO(CreateGradeProps):
    pass


class GradeResponseDTO(GradeProps):
    pass


class GradeListParams(PageRequestDTO):
    pass
