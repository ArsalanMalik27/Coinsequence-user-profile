from uuid import UUID

import structlog

from app.api.api_v1.student.dto.activity import UpdateActivityDTO

from app.api.api_v1.student.dto.activity import (
    CreateActivityDTO,
    ActivityResponseDTO,
    UpdateActivityDTO
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.activity import ActivityProps,CreateActivityProps,Activity
from app.domain.student.repository.db.activity import ActivityRepository
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def update_activity_usecase(
    update_activity_dto_list: list[UpdateActivityDTO],
    activity_repo: ActivityRepository,
    user_profile_props: UserProfileProps,
) -> list[ActivityProps]:
    updated_activities = []
    created_activities = []
    deleted_activities = []

    activity_list = await activity_repo.get_all_activities(user_profile_props.id)
    for update_activity_dto in update_activity_dto_list:
        if not update_activity_dto.id:
            activity_props = CreateActivityProps(**update_activity_dto.dict(exclude={'id','deleted'}))
            activity = Activity.create_from(props=activity_props, profile_id=user_profile_props.id)
            activity_exists = any(activity.props.activity_id == act_item.activity_id for act_item in activity_list)
            if activity_exists:
                raise DomainError("Activity Already Exist")
            created_activities += [activity.props]
        else:
            existing_activity = next(filter(lambda activity_props: (
                    update_activity_dto.id == activity_props.id
            ), activity_list), None)
            if not existing_activity:
                logger.info(
                    "[UpdateActivityUsecase: attempt to update non-existing Activity]",
                    data=user_profile_props,
                )
                raise DomainError("Activity Doesn't Exist")
            activities = list(filter(lambda activity_props: (
                    update_activity_dto.activity_id == activity_props.activity_id
            ), activity_list))
            if existing_activity.activity_id != update_activity_dto.activity_id and len(activities) > 0:
                raise DomainError("Activity Already Exist")
            update_activity_props = CreateActivityProps(**update_activity_dto.dict(exclude={'id', 'deleted'}))
            activity = Activity(props=existing_activity)
            activity.update_from(update_activity_props)
            if update_activity_dto.deleted:
                activity.delete_activity()
                deleted_activities += [activity.props]
            else:
                await activity_repo.update_activity(activity.props, user_profile_props.id)
                updated_activities += [activity.props]
    await activity_repo.bulk_create(created_activities)
    await activity_repo.bulk_delete(user_profile_props.id, deleted_activities)

    return created_activities + updated_activities + deleted_activities