import structlog

from app.api.api_v1.student.dto.voluntary import CreateVoluntaryDTO
from app.domain.student.data.voluntary import (
    CreateVoluntaryProps,
    VoluntaryProps,
    Voluntary
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.voluntary import VoluntaryRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.auth import AuthUser

logger = structlog.get_logger()


async def get_voluntary_list_usecase(
    userprofile_props: UserProfileProps,
    voluntary_repo: VoluntaryRepository,
) -> list:
    voluntary_list = await voluntary_repo.get_all_voluntaries(userprofile_props.id)
    return voluntary_list