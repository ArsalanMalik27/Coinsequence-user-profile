from uuid import UUID
import structlog


from app.domain.student.data.profile import UserProfileProps
from app.repository.db.award import AwardDBRepository
from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def delete_award_usecase(
    award_id: UUID,
    userprofile_props: UserProfileProps,
    award_repo: AwardDBRepository,
) -> None:
    award_props = await award_repo.get_by_id(award_id)
    if not award_props or award_props.profile_id != userprofile_props.id:
        logger.info(
            "[UpdateUserProfileUsecase: attempt to delete Award which is not owned]",
            data=userprofile_props,
        )
        raise DomainError("Invalid Profile Id")
    rows_effected = await award_repo.delete_award(
        award_id, userprofile_props.id
    )
    if not rows_effected:
        logger.info(
            "[UpdateUserProfileUsecase: attempt to delete non-existing Award]",
            data=award_props,
        )
        raise DomainError("Invalid Award Id")
