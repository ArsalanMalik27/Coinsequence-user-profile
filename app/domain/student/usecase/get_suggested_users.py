import structlog

from app.api.api_v1.student.dto.profile import SuggestedUsersParams
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.domain.data.page import Page

logger = structlog.get_logger()


async def get_suggested_users_usecase(
    user_profile_props: UserProfileProps,
    suggested_user_params: SuggestedUsersParams,
    user_profile_repo: UserProfileRepository,
    connection_repo: ConnectionRepository,
) -> Page[UserProfileProps]:
    connections_props = await connection_repo.get_connections_by_profile_id(user_profile_props.id)
    connected_profile_ids = []
    for connection_props in connections_props:
        connected_profile_ids.append(connection_props.user_a)
        connected_profile_ids.append(connection_props.user_b)
    connected_profile_ids = list(set(connected_profile_ids))
    exclude_profile_ids = connected_profile_ids if not suggested_user_params.is_connected else []
    include_profile_ids = connected_profile_ids or [user_profile_props.id] if suggested_user_params.is_connected else []
    print('---------------->', include_profile_ids)
    user_profile_props_page = await user_profile_repo.get_suggested_users(
        user_profile_props.user_id,
        include_profile_ids,
        exclude_profile_ids,
        suggested_user_params.page,
        suggested_user_params.page_size,
        suggested_user_params.query
    )
    return user_profile_props_page
