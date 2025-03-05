from uuid import UUID
import structlog


from app.domain.student.data.profile import UserProfileProps
from app.repository.db.roles import RolesDBRepository
from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def delete_roles_usecase(
    roles_id: UUID,
    userprofile_props: UserProfileProps,
    roles_repo: RolesDBRepository,
) -> None:
    roles_props = await roles_repo.get_by_id(roles_id)
    if not roles_props or roles_props.profile_id != userprofile_props.id:
        logger.info(
            "[UpdateUserProfileUsecase: attempt to delete Roles that is not owned]",
            data=userprofile_props,
        )
        raise DomainError("Invalid Profile Id")
    rows_effected = await roles_repo.delete_roles(
        roles_id, userprofile_props.id
    )
    if not rows_effected:
        logger.info(
            "[UpdateUserProfileUsecase: attempt to delete non-existing Roles]",
            data=roles_props,
        )
        raise DomainError("Invalid Roles Id")
