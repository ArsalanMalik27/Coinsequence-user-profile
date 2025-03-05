from uuid import UUID

import structlog

from app.api.api_v1.connections.dto.connection_request import ConnectionsRequestParams
from app.domain.connections.data.connection_request import ConnectionRequestProps
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)
from app.domain.student.data.profile import UserProfileProps
from app.shared.domain.data.page import Page

logger = structlog.get_logger()


async def get_connection_requests_usecase(
    user_profile_props: UserProfileProps,
    connection_request_repo: ConnectionRequestRepository,
    connection_request_params: ConnectionsRequestParams,
) -> Page[ConnectionRequestProps]:
    connection_requests_props = await connection_request_repo.filter_by_profile_id(
        user_profile_props.id,
        connection_request_params.status,
        connection_request_params.page,
        connection_request_params.page_size,
        connection_request_params.query,
    )
    return connection_requests_props
