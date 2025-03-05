import structlog
from uuid import UUID

from app.api.api_v1.student.dto.award import CreateAwardDTO
from app.domain.student.data.award import (
    CreateAwardProps,
    AwardProps,
    Award
)
from app.domain.connections.data.connection import ConnectionProps

from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType, PrivacyType
from app.domain.student.repository.db.award import AwardRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.auth import AuthUser
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType, ProfilePrivacyProps

logger = structlog.get_logger()


async def get_other_award_list_usecase(
    profile_id: UUID,
    award_repo: AwardRepository,
    profile_privacy_props: ProfilePrivacyProps,
    connected_profiles: ConnectionProps,

) -> list:
    awards_list = await award_repo.get_all_awards(profile_id)
    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == 'AWARD':
            if profile_privacy.privacy_type.value == "PUBLIC":
                return awards_list
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles < 1:
                    return []
                return awards_list
            elif profile_privacy.privacy_type.value == "PRIVATE":
                return []