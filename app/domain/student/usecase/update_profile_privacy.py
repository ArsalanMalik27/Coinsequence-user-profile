from uuid import UUID

import structlog

from app.api.api_v1.student.dto.profile import UpdateProfilePrivacyDTO
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfilePrivacyProps
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository

logger = structlog.get_logger()


async def update_profile_privacy_usecase(
    update_profile_privacy_dto: UpdateProfilePrivacyDTO,
    profile_privacy_props: ProfilePrivacyProps,
    profile_privacy_repo: ProfilePrivacyRepository,
) -> list[ProfilePrivacyProps]:
    updated_profile_privacies_props = []
    update_profile_privacy_dto_dict = update_profile_privacy_dto.dict()
    for profile_privacy_props in profile_privacy_props:
        profile_privacy = ProfilePrivacy(props=profile_privacy_props)
        profile_privacy.update_profile_privacy(
            profile_privacy_props.profile_section_type,
            update_profile_privacy_dto_dict.get(profile_privacy_props.profile_section_type.value.lower(), profile_privacy_props.privacy_type)
        )
        await profile_privacy_repo.update(profile_privacy.props)
        updated_profile_privacies_props.append(profile_privacy.props)
    return updated_profile_privacies_props
