import structlog

from app.api.api_v1.student.dto.grade import CreateGradeDTO
from app.domain.student.data.grade import Grade, GradeProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.grade import GradeRepository
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def create_grade_usecase(
    create_grade_dto: CreateGradeDTO,
    grade_repo: GradeRepository,
    profile_props: UserProfileProps,
) -> GradeProps:
    if create_grade_dto.gpa > create_grade_dto.max_gpa:
        raise DomainError("Invalid GPA Range")
    if  len(create_grade_dto.courses) != len(set(create_grade_dto.courses)):
        raise DomainError("Courses are not unique")
    grade_count = await grade_repo.grade_count_by_level(profile_props.id, create_grade_dto.level)
    if grade_count >= 1:
        raise DomainError("Grade Already Exist")
    grade = Grade.create_from(create_grade_dto, profile_props.id)
    await grade_repo.create(grade.props)
    return grade.props
