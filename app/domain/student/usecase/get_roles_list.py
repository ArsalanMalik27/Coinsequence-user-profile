import structlog

from app.api.api_v1.student.dto.award import CreateAwardDTO
from app.domain.student.data.roles import (
    CreateRolesProps,
    RolesProps,
    Roles
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.roles import RolesRepository
from app.domain.student.repository.db.profile import UserProfileRepository

logger = structlog.get_logger()

async def get_roles_list_usecase(
    profile_props: UserProfileProps,
    roles_repo: RolesRepository,
)->list:
    roles_props = await roles_repo.get_all_roles(profile_props.id)
    return roles_props