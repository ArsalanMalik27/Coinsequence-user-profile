from uuid import UUID

import structlog

from app.container import Container
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def get_user_profile_usecase(
    user_id: UUID, user_profile_repo: UserProfileRepository
) -> UserProfileProps:
    user_profile_props = await user_profile_repo.get_by_user_id(user_id)
    if not user_profile_props:
        logger.info(
            "[GetUserProfileUsecase: profile with this ID does not exist]",
            data=user_id,
        )
        raise DomainError("Profile for this user does not exist")
    return user_profile_props
