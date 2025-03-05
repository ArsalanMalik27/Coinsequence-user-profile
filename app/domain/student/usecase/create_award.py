import structlog

from app.api.api_v1.student.dto.award import CreateAwardDTO
from app.domain.student.data.award import (
    CreateAwardProps,
    AwardProps,
    Award
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.award import AwardRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.auth import AuthUser
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def create_award_usecase(
    userprofile_props: UserProfileProps,
    create_award_dto: CreateAwardDTO,
    award_repo: AwardRepository,
) -> AwardProps:
    if len(create_award_dto.description) > 600:
        raise DomainError("Description is too long")
    award_props = CreateAwardProps(**create_award_dto.dict())
    award = Award.create_from(props=award_props,profile_id=userprofile_props.id)
    await award_repo.create(award.props)
    return award.props
