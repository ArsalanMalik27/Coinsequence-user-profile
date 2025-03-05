from uuid import UUID

import structlog

from app.api.api_v1.student.dto.education import EducationParams
from app.domain.student.data.education import EducationProps
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.education import EducationDBRepository
from app.shared.domain.data.page import Page
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def list_all_education_usecase(
    userprofile_props: UserProfileProps,
    education_repo: EducationDBRepository,
) -> list[EducationProps]:
    educations = await education_repo.filter_by_profile_id(
        userprofile_props.id,
    )
    return educations
