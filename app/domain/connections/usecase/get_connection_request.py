from uuid import UUID

from app.domain.connections.data.connection_request import (
    ConnectionRequestProps,
    ConnectionRequestStatus,
)
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)


async def get_connection_request_usecase(
    profile_a_id: UUID,
    profile_b_id: UUID,
    connection_request_repo: ConnectionRequestRepository
) -> ConnectionRequestProps:
    connection_request_props = await connection_request_repo.get_by_profile_ids(
        profile_a_id, profile_b_id, ConnectionRequestStatus.PENDING)
    return connection_request_props
