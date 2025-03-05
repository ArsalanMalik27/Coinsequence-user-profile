from uuid import UUID

import structlog
from app.domain.student.repository.db.children_profile import ChildrenProfileRepository
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.profile import UserProfileRepository
from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def list_all_children_profile_usecase(
    userprofile_props: UserProfileProps,
    user_profile_repo: UserProfileRepository,
    children_profile: ChildrenProfileRepository,
) -> list[UserProfileProps]:
    children_list = await children_profile.filter_by_parent_id(
        userprofile_props.id,
    )
    children_profile_ids = []
    for child_props in children_list:
        children_profile_ids.append(child_props.child_id)
    if not children_profile_ids:
        return []
    children_profile_props = await user_profile_repo.get_profiles(include_profile_ids=children_profile_ids)
    return children_profile_props
