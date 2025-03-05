from uuid import UUID

import structlog
from fastapi import UploadFile

from app.domain.student.data.profile import UserProfile, UserProfileProps
from app.domain.student.event.user_profile_updated import UserProfileUpdated
from app.domain.student.repository.db.profile import UserProfileRepository
from app.infra.config import settings
from app.shared.repository.event_client import EventClient
from app.shared.repository.storage_client import StorageClient
from app.shared.utils.error import DomainError

logger = structlog.get_logger()
S3_PROFILE_MEDIA = "profile"


async def upload_profile_pic_usecase(
    user_profile_props: UserProfileProps,
    file: UploadFile,
    user_profile_repo: UserProfileRepository,
    event_client: EventClient,
    store_client: StorageClient,
) -> UserProfileProps:
    upload_files = await store_client.upload(S3_PROFILE_MEDIA, user_profile_props.user_id, [file])
    user_profile = UserProfile(props=user_profile_props)
    user_profile.update_profile_pic(upload_files[0])
    await user_profile_repo.update_profile(user_profile.props)
    event = UserProfileUpdated.from_entity(entity=user_profile.props)
    await event_client.publish(topic_name=settings.SNS.PROFILE_UPDATED, data=event)
    return user_profile.props
