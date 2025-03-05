from uuid import UUID

import structlog
from app.api.api_v1.student.dto.voluntary import (
    CreateVoluntaryDTO,
    VoluntaryResponseDTO,
    UpdateVoluntaryDTO
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.voluntary import VoluntaryProps,CreateVoluntaryProps,Voluntary
from app.domain.student.repository.db.voluntary import VoluntaryRepository
from app.shared.utils.error import DomainError
from datetime import datetime

logger = structlog.get_logger()


async def update_voluntary_usecase(
    voluntary_id: UUID,
    update_voluntary_dto: UpdateVoluntaryDTO,
    voluntary_repo: VoluntaryRepository,
    user_profile_props: UserProfileProps,
) -> VoluntaryProps:
    current_date = datetime.now().date()
    if update_voluntary_dto.start_date >= update_voluntary_dto.end_date or update_voluntary_dto.start_date > current_date:
        raise DomainError('Invalid Date Range')
    if len(update_voluntary_dto.description) > 600:
        raise DomainError("Description is too long")
    existing_voluntary = await voluntary_repo.get_by_id(voluntary_id)
    if not existing_voluntary or existing_voluntary.profile_id != user_profile_props.id:
        logger.info(
            "[UpdateVoluntaryUsecase: attempt to update non-existing voluntary]",
            data=user_profile_props,
        )
        raise DomainError("Invalid voluntary")

    update_voluntary_props = CreateVoluntaryProps(**update_voluntary_dto.dict())
    voluntary_props = Voluntary(props=existing_voluntary)
    voluntary_props.update_from(update_voluntary_props)
    await voluntary_repo.update_voluntary(voluntary_props.props, user_profile_props.id)
    return voluntary_props.props
