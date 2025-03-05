import structlog

from app.api.api_v1.student.dto.profile import CreateUserProfileDTO
from app.domain.student.data.profile import UserProfile, UserProfileProps
from app.domain.student.data.profile_privacy import (
    PrivacyType,
    ProfilePrivacy,
    ProfileSectionType,
)
from app.domain.student.event.user_profile_updated import UserProfileUpdated
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.infra.config import settings
from app.shared.repository.event_client import EventClient
from app.shared.utils.auth import AuthUser
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def create_user_profile_usecase(
    user: AuthUser,
    create_profile_dto: CreateUserProfileDTO,
    user_profile_repo: UserProfileRepository,
    profile_privacy_repo: ProfilePrivacyRepository,
    event_client: EventClient,
) -> UserProfileProps:
    user_profile = UserProfile.from_user(user, create_profile_dto.profile_type)
    existing_user_profile = await user_profile_repo.get_by_user_id(user.id)
    if existing_user_profile:
        logger.info(
            "[CreateUserProfileUsecase: attempt to recreate existing user profile]",
            data=user,
        )
        raise DomainError("Profile for this user is already created")
    await user_profile_repo.create_profile(user_profile.props)
    profile_privacies_props = []
    for profile_section in ProfileSectionType:
        profile_privacy = ProfilePrivacy.from_user(
            user_profile.props.id,
            PrivacyType.PUBLIC,
            profile_section,
        )
        profile_privacies_props.append(profile_privacy.props)
    await profile_privacy_repo.bulk_create(profile_privacies_props)
    # event = UserProfileUpdated.from_entity(user_profile.props)
    # await event_client.publish(
    #     topic_name=settings.SNS.PROFILE_UPDATED, data=event
    # )
    return user_profile.props
