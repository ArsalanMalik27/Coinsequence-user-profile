from uuid import UUID
import structlog


from app.domain.student.data.profile import UserProfileProps
from app.repository.db.activity import ActivityDBRepository
from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def delete_activity_usecase(
    activity_id: UUID,
    userprofile_props: UserProfileProps,
    activity_repo: ActivityDBRepository,
) -> None:
    activity_props = await activity_repo.get_by_id(activity_id)
    if not activity_props or activity_props.profile_id != userprofile_props.id:
        logger.info(
            "[UpdateUserProfileUsecase: attempt to delete Activity which is not owned]",
            data=userprofile_props,
        )
        raise DomainError("Invalid Profile Id")
    await activity_repo.delete_activity(
        activity_id, userprofile_props.id
    )