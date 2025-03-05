from uuid import UUID

import structlog

from app.api.api_v1.student.dto.work import CreateWorkDTO
from app.domain.connections.data.connection import ConnectionProps
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import (
    ProfilePrivacy,
    ProfilePrivacyProps,
    ProfileSectionType,
)
from app.domain.student.data.work import CreateWorkProps, Work, WorkProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.student.repository.db.work import WorkRepository
from app.shared.utils.auth import AuthUser

logger = structlog.get_logger()


async def get_other_work_list_usecase(
    profile_id: UUID,
    work_repo: WorkRepository,
    profile_privacy_props: ProfilePrivacyProps,
    connected_profiles: ConnectionProps,
) -> list:
    work_list = await work_repo.get_all_work(profile_id)
    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == "INTERNSHIP":
            if profile_privacy.privacy_type.value == "PUBLIC":
                return work_list
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles < 1:
                    return []
                return work_list
            elif profile_privacy.privacy_type.value == "PRIVATE":
                return []
