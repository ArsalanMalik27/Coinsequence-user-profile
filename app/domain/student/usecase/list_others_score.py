from uuid import UUID
import structlog

from app.domain.student.data.score import ScoreProps
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.score import ScoreDBRepository

from app.shared.utils.error import DomainError

from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType,ProfilePrivacyProps
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.connections.repository.db.connection import ConnectionRepository

from app.domain.connections.data.connection import ConnectionProps
logger = structlog.get_logger()


async def list_others_score_usecase(
        profile_id: UUID,
        profile_privacy_props: ProfilePrivacyProps,
        connected_profiles: ConnectionProps,
        score_repo: ScoreDBRepository,
)->list[ScoreProps]:
    scores = await score_repo.get_score_list(profile_id)
    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == 'SCORE':
            if profile_privacy.privacy_type.value == "PUBLIC":
                return scores
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles < 1:
                    return []
                return scores
            elif profile_privacy.privacy_type.value == "PRIVATE":
                return []
