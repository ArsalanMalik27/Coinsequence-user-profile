from uuid import UUID

import structlog

from app.api.api_v1.student.dto.roles import UpdateRolesDTO
from app.domain.student.data.roles import (
    CreateRolesProps,
    Roles,
    RolesProps,
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.roles import RolesRepository
from app.shared.utils.error import DomainError
from datetime import datetime
logger = structlog.get_logger()


async def update_roles_usecase(
    roles_id: UUID,
    update_roles_dto: UpdateRolesDTO,
    roles_repo: RolesRepository,
    user_profile_props: UserProfileProps,
) -> RolesProps:
    current_date = datetime.now().date()
    if update_roles_dto.start_date >= update_roles_dto.end_date or update_roles_dto.start_date > current_date:
        raise DomainError("Invalid Domain Range")
    if len(update_roles_dto.description) > 600:
        raise DomainError("Description is too long")
    existing_roles = await roles_repo.get_by_id(roles_id)
    if not existing_roles or existing_roles.profile_id != user_profile_props.id:
        logger.info(
            "[UpdateRolesUsecase: attempt to update non-existing Roles]",
            data=user_profile_props,
        )
        raise DomainError("Invalid Roles")

    upgrade_roles_props = CreateRolesProps(**update_roles_dto.dict())
    roles_props = Roles(props=existing_roles)

    roles_props.update_from(upgrade_roles_props)
    await roles_repo.update_roles(roles_props.props, user_profile_props.id)
    return roles_props.props
