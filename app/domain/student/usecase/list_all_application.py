from uuid import UUID

import structlog

from app.api.api_v1.student.dto.education import EducationParams
from app.domain.student.data.application import ApplicationProps
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.application import ApplicationDBRepository
from app.masterdata_shared.api_client import MasterdataAPIClient
from app.shared.domain.data.page import Page
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def list_all_application_usecase(
    profile_id: str,
    application_repo: ApplicationDBRepository,
) -> list[ApplicationProps]:
    applications = await application_repo.filter_by_profile_id(profile_id)
    return applications
