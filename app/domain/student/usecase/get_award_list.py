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

logger = structlog.get_logger()


async def get_award_list_usecase(
    userprofile_props: UserProfileProps,
    award_repo: AwardRepository,
) -> list:
    awards_list = await award_repo.get_all_awards(userprofile_props.id)
    return awards_list