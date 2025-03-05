from uuid import UUID
import structlog


from app.domain.student.data.profile import UserProfileProps
from app.repository.db.voluntary import VoluntaryDBRepository
from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def delete_voluntary_usecase(
    voluntary_id: UUID,
    userprofile_props: UserProfileProps,
    voluntary_repo: VoluntaryDBRepository,
) -> None:
    voluntary_props = await voluntary_repo.get_by_id(voluntary_id)
    if not voluntary_props or voluntary_props.profile_id != userprofile_props.id:
        logger.info(
            "[UpdateUserProfileUsecase: attempt to delete voluntary work which is not owned]",
            data=userprofile_props,
        )
        raise DomainError("Invalid voluntary work")
    await voluntary_repo.delete_voluntary(
        voluntary_id, userprofile_props.id
    )
