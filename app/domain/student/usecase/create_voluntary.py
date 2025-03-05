import structlog

from app.api.api_v1.student.dto.voluntary import CreateVoluntaryDTO
from app.domain.student.data.voluntary import (
    CreateVoluntaryProps,
    Voluntary,
    VoluntaryProps,
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.voluntary import VoluntaryRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.auth import AuthUser
from app.shared.utils.error import DomainError
from datetime import datetime


logger = structlog.get_logger()


async def create_voluntary_usecase(
    userprofile_props: UserProfileProps,
    create_voluntary_dto: CreateVoluntaryDTO,
    voluntary_repo: VoluntaryRepository,
) -> VoluntaryProps:
    current_date = datetime.now().date()
    if create_voluntary_dto.start_date >= create_voluntary_dto.end_date or create_voluntary_dto.start_date > current_date:
        raise DomainError("Invalid Domain Range")
    if len(create_voluntary_dto.description) > 600:
        raise DomainError("Description is too long")
    voluntary_props = CreateVoluntaryProps(**create_voluntary_dto.dict())
    voluntary = Voluntary.create_from(props=voluntary_props,profile_id=userprofile_props.id)
    await voluntary_repo.create_voluntary(voluntary.props)
    return voluntary.props
