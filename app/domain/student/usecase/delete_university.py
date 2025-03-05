from uuid import UUID
import structlog


from app.domain.student.data.profile import UserProfileProps
from app.repository.db.college_university import UniversityDBRepository
from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def delete_university_usecase(
    university_id: UUID,
    userprofile_props: UserProfileProps,
    university_repo: UniversityDBRepository,
) -> None:
    university_props = await university_repo.get_by_id(university_id)
    if not university_props or university_props.profile_id != userprofile_props.id:
        logger.info(
            "[UpdateUserProfileUsecase: attempt to delete non owned details]",
            data=userprofile_props,
        )
        raise DomainError("Invalid Profile Id")
    await university_repo.delete_university(university_id, userprofile_props.id)
