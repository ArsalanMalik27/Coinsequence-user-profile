from uuid import UUID

import structlog

from app.api.api_v1.student.dto.grade import UpdateGradeDTO
from app.domain.student.data.grade import CreateGradeProps, Grade, GradeProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.grade import GradeRepository
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def update_grade_usecase(
    grade_id: UUID,
    update_grade_dto: UpdateGradeDTO,
    grade_repo: GradeRepository,
    profile_props: UserProfileProps,
) -> GradeProps:
    if update_grade_dto.gpa > update_grade_dto.max_gpa or len(update_grade_dto.courses) != len(set(update_grade_dto.courses)):
        raise DomainError("Invalid GPA Range or Courses")
    existing_grade = await grade_repo.get_by_id(grade_id)
    if not existing_grade or profile_props.id != existing_grade.profile_id:
        logger.info(
            "[UpdateGradeUsecase: attempt to update non-existing Grade]",
            data=existing_grade,
        )
        raise DomainError("Invalid Grade")
    grade_count = await grade_repo.grade_count_by_level(profile_props.id, update_grade_dto.level)
    if update_grade_dto.level != existing_grade.level:
        if grade_count >= 1:
            raise DomainError("Grade Already Exist")
    else:
        if grade_count > 1:
            raise DomainError("Grade Already Exist")
    up_grade_props = CreateGradeProps(**update_grade_dto.dict())
    grade = Grade(props=existing_grade)
    grade.update_from(up_grade_props)
    await grade_repo.update_grade(grade.props)
    return grade.props
