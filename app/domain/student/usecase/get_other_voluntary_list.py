from uuid import UUID
import structlog

from app.api.api_v1.student.dto.voluntary import CreateVoluntaryDTO
from app.domain.student.data.voluntary import (
    CreateVoluntaryProps,
    VoluntaryProps,
    Voluntary
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType, ProfilePrivacyProps

from app.domain.student.repository.db.voluntary import VoluntaryRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.shared.utils.auth import AuthUser
from app.domain.connections.data.connection import ConnectionProps

logger = structlog.get_logger()


async def get_other_voluntary_list_usecase(
    profile_id: UUID,
    profile_privacy_props: ProfilePrivacyProps,
    connected_profiles: ConnectionProps,
    voluntary_repo: VoluntaryRepository,
)-> list:
    voluntary_list = await voluntary_repo.get_all_voluntaries(profile_id)
    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == 'VOLUNTARY_WORK':
            if profile_privacy.privacy_type.value == "PUBLIC":
                return voluntary_list
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles < 1:
                    return []
                return voluntary_list
            elif profile_privacy.privacy_type.value == "PRIVATE":
                return []