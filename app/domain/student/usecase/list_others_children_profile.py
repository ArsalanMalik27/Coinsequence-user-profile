from uuid import UUID

import structlog
from app.domain.student.repository.db.children_profile import ChildrenProfileRepository
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacyProps
from app.domain.connections.data.connection import ConnectionProps
from app.repository.db.profile import UserProfileRepository

from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def list_others_children_profile_usecase(
    userprofile_props: UserProfileProps,
    user_profile_repo: UserProfileRepository,
    children_profile: ChildrenProfileRepository,
    profile_privacy_props: ProfilePrivacyProps,
    connected_profiles: ConnectionProps,
) -> list[UserProfileProps]:

    flag = False

    for profile_privacy in profile_privacy_props:
        if profile_privacy.profile_section_type.value == 'CHILDREN':
            if profile_privacy.privacy_type.value == "PUBLIC":
                flag = True
            elif profile_privacy.privacy_type.value == "CONNECTION":
                if connected_profiles > 0:
                    flag = True

    if flag:
        children_list = await children_profile.filter_by_parent_id(
            userprofile_props.id,
        )
        children_profile_ids = []
        for child_props in children_list:
            children_profile_ids.append(child_props.child_id)
        children_profile_props_list = await user_profile_repo.get_profiles(include_profile_ids=children_profile_ids)
        return children_profile_props_list
    else:
        return []