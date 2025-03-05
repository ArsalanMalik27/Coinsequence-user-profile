import structlog
from uuid import UUID

from app.api.api_v1.student.dto.activity import CreateActivityDTO
from app.domain.student.data.activity import (
    CreateActivityProps,
    ActivityProps,
    Activity
)
from app.domain.connections.data.connection import ConnectionProps

from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType,ProfilePrivacyProps
from app.domain.student.repository.db.activity import ActivityRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.auth import AuthUser

logger = structlog.get_logger()

async def get_other_activity_list_usecase(
    profile_id: UUID,
    activity_repo: ActivityRepository,
    profile_privacy_props: ProfilePrivacyProps,
    connected_profiles: ConnectionProps,
) -> list:
    activity_list = await activity_repo.get_all_activities(profile_id)
    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == 'ACTIVITY':
            if profile_privacy.privacy_type.value == "PUBLIC":
                return activity_list
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles < 1:
                    return []
                return activity_list
            elif profile_privacy.privacy_type.value == "PRIVATE":
                return []
    return []