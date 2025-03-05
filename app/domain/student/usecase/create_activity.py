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
from app.shared.utils.auth import AuthUser

logger = structlog.get_logger()


async def create_activity_usecase(
    userprofile_props: UserProfileProps,
    create_activity_dto_list: list[CreateActivityDTO],
    activity_repo: ActivityRepository,
) -> ActivityProps:
    activity_props_list = []
    for create_activity_dto in create_activity_dto_list:
        activity_id_count = await activity_repo.get_by_activity_id_count(userprofile_props.id, create_activity_dto.activity_id)
        if activity_id_count < 1:
            activity_props = CreateActivityProps(**create_activity_dto.dict())
            activity = Activity.create_from(props=activity_props,profile_id=userprofile_props.id)
            await activity_repo.create(activity.props)
            activity_props_list += [activity.props]
    return activity_props_list
