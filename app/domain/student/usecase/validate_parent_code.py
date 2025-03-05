from app.domain.connections.data.connection_request import (
    ConnectionRequest,
    CreateConnectionRequestProps,
)
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)

from app.domain.student.repository.db.children_profile import (
ChildrenProfileRepository
)
from app.domain.student.data.profile import (
    UserProfile,
    UserProfileProps,
    UserProfileType,
)
from app.domain.student.data.children_profile import Children_Profile,ChildrenProfileProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.error import DomainError
from app.domain.connections.usecase.create_connection_request import create_connection_request_usecase
from app.api.api_v1.connections.dto.connection_request import CreateConnectionRequestDTO

async def validate_parent_code_usecase(
        parent_code: str,
        parent_profile_props: UserProfileProps,
        user_profile_repo: UserProfileRepository,
        connection_request_repo: ConnectionRequestRepository,
        children_profile_repo: ChildrenProfileRepository
) -> None:
    child_userprofile_props = await user_profile_repo.get_by_parent_code(parent_code)
    if not child_userprofile_props:
        raise DomainError("Parent code invalid")
    children_count = await children_profile_repo.count_children_by_child_id(child_userprofile_props.id)
    if children_count >= 2:
        raise DomainError("Parents Already Exist")
    child_profile_props = Children_Profile.from_users(child_userprofile_props.id,
                                                      parent_profile_props.id)
    await children_profile_repo.create(child_profile_props.props)
    create_connection_request_dto = CreateConnectionRequestDTO(receiver_id=child_userprofile_props.id)
    await create_connection_request_usecase(
        parent_profile_props.id,
        create_connection_request_dto,
        connection_request_repo
    )
    user_profile = UserProfile(props=child_userprofile_props)
    user_profile.update_parent_code()
    await user_profile_repo.update_profile(user_profile.props)
