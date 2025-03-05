import structlog

from app.api.api_v1.student.dto.activity import CreateActivityDTO
from app.domain.student.data.activity import (
    CreateActivityProps,
    ActivityProps,
    Activity
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.activity import ActivityRepository
from app.domain.student.repository.db.profile import UserProfileRepository

logger = structlog.get_logger()


async def get_activity_list_usecase(
    userprofile_props: UserProfileProps,
    activity_repo: ActivityRepository,
) -> list:
    activity_list = await activity_repo.get_all_activities(userprofile_props.id)
    return activity_list