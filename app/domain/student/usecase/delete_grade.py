from uuid import UUID
import structlog

from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.grade import GradeRepository
from app.shared.utils.error import DomainError
from app.shared.utils.auth import AuthUser

logger = structlog.get_logger()


async def delete_grade_usecase(
    grade_id: UUID,
    grade_repo: GradeRepository,
    profile_props: UserProfileProps,
) -> None:
    grade_props = await grade_repo.get_by_id(grade_id)
    if not grade_props or profile_props.id != grade_props.profile_id:
        logger.info(
            "[DeleteGradeUsecase: attempt to delete non-existing Grade]",
            data=grade_props,
        )
        raise DomainError("Invalid Grade")
    await grade_repo.delete(grade_id)
