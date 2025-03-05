from uuid import UUID
import structlog

from app.domain.student.data.test import TestProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType,ProfilePrivacyProps
from app.repository.db.test import TestDBRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.connections.data.connection import ConnectionProps

from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def list_others_test_score_usecase(
        profile_id: UUID,
        test_repo: TestDBRepository,
        profile_privacy_props: ProfilePrivacyProps,
        connected_profiles: ConnectionProps,
)->list[TestProps]:
    test_list = await test_repo.get_test_list_by_profile_id(profile_id)
    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == 'SCORE':
            if profile_privacy.privacy_type.value == "PUBLIC":
                return test_list
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles < 1:
                    return []
                return test_list
            elif profile_privacy.privacy_type.value == "PRIVATE":
                return []