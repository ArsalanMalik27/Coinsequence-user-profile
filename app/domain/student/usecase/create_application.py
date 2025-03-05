import structlog
from uuid import UUID

from app.api.api_v1.student.dto.application import CreateApplicationDTO
from app.domain.student.data.application import CreateApplicationProps, ApplicationProps, Application
from app.domain.student.repository.db.application import ApplicationRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.data.profile import UserProfileProps

from app.infra.config import settings
from app.shared.repository.event_client import EventClient
from app.shared.utils.auth import AuthUser

logger = structlog.get_logger()


async def create_application_usecase(
    userprofile_props: UserProfileProps,
    create_application_dto: CreateApplicationDTO,
    application_repo: ApplicationRepository,
) -> ApplicationProps:
    application_props = CreateApplicationProps(**create_application_dto.dict())
    application = Application.create_from(props=application_props, profile_id=userprofile_props.id)
    await application_repo.create(application.props)
    return application.props


