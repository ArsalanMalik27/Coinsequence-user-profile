from uuid import UUID

import structlog

from app.api.api_v1.student.dto.profile import UpdateUserProfileDTO
from app.domain.student.data.profile import ProfileProps, UserProfile, UserProfileProps
from app.domain.student.event.user_profile_updated import UserProfileUpdated
from app.domain.student.repository.db.profile import UserProfileRepository
from app.infra.config import settings
from app.shared.domain.repository.event_client import EventClient
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def update_user_profile_usecase(
    existing_user_profile: UserProfileProps,
    update_user_profile_dto: UpdateUserProfileDTO,
    user_profile_repo: UserProfileRepository,
    event_client: EventClient
) -> UserProfileProps:
    profile_props = ProfileProps(**update_user_profile_dto.dict())
    user_profile = UserProfile(props=existing_user_profile)
    user_profile.update_from(profile_props)
    await user_profile_repo.update_profile(user_profile.props)
    event = UserProfileUpdated.from_entity(user_profile.props)
    await event_client.publish(
        topic_name=settings.SNS.PROFILE_UPDATED, data=event
    )
    return user_profile.props
