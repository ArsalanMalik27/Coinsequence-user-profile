from uuid import UUID
import structlog


from app.domain.student.data.profile import UserProfileProps
from app.repository.db.education import EducationDBRepository
from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def delete_education_usecase(
    education_id: UUID,
    userprofile_props: UserProfileProps,
    education_repo: EducationDBRepository,
) -> None:
    education_props = await education_repo.get_by_id(education_id)

    if not education_props or education_props.profile_id != userprofile_props.id:
        logger.info(
            "[UpdateUserProfileUsecase: attempt to delete education by nonowner]",
            data=userprofile_props,
        )
        raise DomainError("Invalid Education Id")
    await education_repo.delete_education(
        education_id, userprofile_props.id
    )
