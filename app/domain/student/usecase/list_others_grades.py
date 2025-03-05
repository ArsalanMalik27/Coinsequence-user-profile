from uuid import UUID
import structlog
from typing import List, Optional

from app.domain.student.data.grade import GradeProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType,ProfilePrivacyProps
from app.domain.student.repository.db.grade import GradeRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.connections.repository.db.connection import ConnectionRepository

from app.domain.connections.data.connection import ConnectionProps


from app.shared.utils.error import DomainError


logger = structlog.get_logger()

async def list_others_grades_usecase(
    profile_id: UUID,
    grade_repo: GradeRepository,
    profile_privacy_props: ProfilePrivacyProps,
    connected_profiles: ConnectionProps,
)-> List[Optional[GradeProps]]:
    grades = await grade_repo.grade_list(profile_id)
    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == 'GRADE':
            if profile_privacy.privacy_type.value == "PUBLIC":
                return grades
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles < 1:
                    return []
                return grades
            elif profile_privacy.privacy_type.value == "PRIVATE":
                return []
