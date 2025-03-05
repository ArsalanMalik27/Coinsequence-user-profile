from uuid import UUID

import structlog

from app.api.api_v1.student.dto.award import UpdateAwardDTO

from app.api.api_v1.student.dto.award import (
    CreateAwardDTO,
    AwardResponseDTO,
    UpdateAwardDTO
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.award import AwardProps,CreateAwardProps,Award
from app.domain.student.repository.db.award import AwardRepository
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def update_award_usecase(
    award_id: UUID,
    update_award_dto: UpdateAwardDTO,
    award_repo: AwardRepository,
    user_profile_props: UserProfileProps,
) -> AwardProps:
    if len(update_award_dto.description) > 600:
        raise DomainError("Description is too long")
    existing_award = await award_repo.get_by_id(award_id)
    if not existing_award or existing_award.profile_id != user_profile_props.id:
        logger.info(
            "[UpdateAwardUsecase: attempt to update non-existing Award]",
            data=user_profile_props,
        )
        raise DomainError("Invalid Award")

    update_award_props = CreateAwardProps(**update_award_dto.dict())
    award_props = Award(props=existing_award)
    award_props.update_from(update_award_props)
    await award_repo.update_award(award_props.props, user_profile_props.id)
    return award_props.props
