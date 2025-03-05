from uuid import UUID
import structlog

from app.api.api_v1.student.dto.education import (
    EducationParams,
)
from app.domain.student.data.education import EducationProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType,ProfilePrivacyProps

from app.repository.db.education import EducationDBRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.connections.repository.db.connection import ConnectionRepository

from app.shared.domain.data.page import Page
from app.shared.utils.error import DomainError
from app.domain.connections.data.connection import ConnectionProps


logger = structlog.get_logger()


async def list_others_education_usecase(
    profile_id: UUID,
    education_repo: EducationDBRepository,
    connected_profiles: ConnectionProps,
    profile_privacy_props: ProfilePrivacyProps,
) -> list[EducationProps]:
    educations = await education_repo.filter_by_profile_id(
        profile_id,
    )
    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == 'EDUCATION':
            if profile_privacy.privacy_type.value == "PUBLIC":
                return educations
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles < 1:
                    return []
                return educations
            elif profile_privacy.privacy_type.value == "PRIVATE":
                return []
