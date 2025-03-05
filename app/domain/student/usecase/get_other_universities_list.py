from uuid import UUID

import structlog

from app.api.api_v1.student.dto.award import CreateAwardDTO
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.student.data.award import Award, AwardProps, CreateAwardProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType, ProfilePrivacyProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.repository.db.college_university import UniversityRepository
from app.shared.utils.auth import AuthUser
from app.domain.connections.data.connection import ConnectionProps

logger = structlog.get_logger()


async def get_other_universities_list_usecase(
    profile_id: UUID,
    university_repo: UniversityRepository,
    profile_privacy_props: ProfilePrivacyProps,
    connected_profiles: ConnectionProps,

)->list:
    universities_list = await university_repo.get_all_universities(profile_id)
    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == 'COLLEGE':
            if profile_privacy.privacy_type.value == "PUBLIC":
                return universities_list
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles < 1:
                    return []
                return universities_list
            elif profile_privacy.privacy_type.value == "PRIVATE":
                return []