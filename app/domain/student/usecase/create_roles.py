import structlog

from app.api.api_v1.student.dto.roles import CreateRolesDTO
from app.domain.student.data.roles import (
    CreateRolesProps,
    Roles,
    RolesProps,
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.roles import RolesRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.auth import AuthUser
from app.shared.utils.error import DomainError
from datetime import datetime

logger = structlog.get_logger()


async def create_roles_usecase(
    userprofile_props: UserProfileProps,
    create_roles_dto: CreateRolesDTO,
    roles_repo: RolesRepository,
) -> RolesProps:
    current_date = datetime.now().date()
    if create_roles_dto.start_date >= create_roles_dto.end_date or create_roles_dto.start_date > current_date:
        raise DomainError("Invalid Date Range")
    if len(create_roles_dto.description) > 600:
        raise DomainError("Description is too long")
    roles_props = CreateRolesProps(**create_roles_dto.dict())
    roles = Roles.create_from(props=roles_props,profile_id=userprofile_props.id)
    await roles_repo.create_roles(roles.props)
    return roles.props
