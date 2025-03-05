from uuid import UUID

from app.api.api_v1.connections.dto.connection import ConnectionsParams
from app.domain.connections.data.connection import ConnectionProps
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.shared.domain.data.page import Page


async def get_connections_usecase(
    profile_id: UUID,
    connection_repo: ConnectionRepository,
    connection_params: ConnectionsParams,
) -> Page[ConnectionProps]:
    connections_props = await connection_repo.filter_by_profile_id(
        profile_id, connection_params.page, connection_params.page_size
    )
    return connections_props
