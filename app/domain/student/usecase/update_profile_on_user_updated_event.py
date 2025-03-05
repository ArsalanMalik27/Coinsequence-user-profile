import structlog

from app.domain.student.data.profile import UserProfile, UserProfileProps
from app.domain.student.event.user_profile_updated import UserProfileUpdated
from app.domain.student.event.user_updated import UserUpdatedData
from app.domain.student.repository.db.profile import UserProfileRepository
from app.infra.config import settings
from app.shared.domain.repository.event_client import EventClient

logger = structlog.get_logger()


async def update_profile_on_user_updated_event_usecase(
    user_updated_data: UserUpdatedData,
    user_profile_repo: UserProfileRepository,
    event_client: EventClient,
) -> UserProfileProps:
    existing_user_profile = await user_profile_repo.get_by_user_id(user_updated_data.id)
    if not existing_user_profile:
        logger.info(
            "[UpdateProfileOnUserUpdatedEventUsecase: attempt to update non-existing"
            " user profile]"
        )
        return
    user_profile = UserProfile(props=existing_user_profile)
    user_profile.update_name(user_updated_data.first_name, user_updated_data.last_name)
    await user_profile_repo.update_profile(user_profile.props)
    event = UserProfileUpdated.from_entity(entity=user_profile.props)
    await event_client.publish(topic_name=settings.SNS.PROFILE_UPDATED, data=event)
    return user_profile.props
