from uuid import UUID

import structlog

from app.container import Container
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def get_user_by_profile_id_usecase(
        profile_id: UUID,
        user_profile_repo: UserProfileRepository
) -> UserProfileProps:
    user_profile_props = await user_profile_repo.get_profile_by_id(profile_id)
    if not user_profile_props:
        logger.info(
            "[GetUserProfileUsecase: profile with this ID does not exist]",
            data=profile_id,
        )
        raise DomainError("Profile for this user does not exist")
    return user_profile_props
