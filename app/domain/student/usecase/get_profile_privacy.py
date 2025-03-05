from uuid import UUID

import structlog

from app.domain.student.data.profile_privacy import ProfilePrivacyProps
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository

logger = structlog.get_logger()

async def get_profile_privacies_usecase(
    profile_id: UUID,
    profile_privacy_repo: ProfilePrivacyRepository,
) -> list[ProfilePrivacyProps]:
    profile_privacies_props = await profile_privacy_repo.filter(profile_id)
    return profile_privacies_props
