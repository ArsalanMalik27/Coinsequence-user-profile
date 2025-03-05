import structlog
from uuid import UUID
from app.api.api_v1.student.dto.award import CreateAwardDTO
from app.domain.student.data.roles import (
    CreateRolesProps,
    RolesProps,
    Roles
)
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType,ProfilePrivacyProps

from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.roles import RolesRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.connections.data.connection import ConnectionProps

logger = structlog.get_logger()

async def get_others_roles_list_usecase(
    profile_id: UUID,
    roles_repo: RolesRepository,
    profile_privacy_props: ProfilePrivacyProps,
    connected_profiles: ConnectionProps,
)->list:
    roles_props = await roles_repo.get_all_roles(profile_id)
    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == 'LEADERSHIP':
            if profile_privacy.privacy_type.value == "PUBLIC":
                return roles_props
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles < 1:
                    return []
                return roles_props
            elif profile_privacy.privacy_type.value == "PRIVATE":
                return []