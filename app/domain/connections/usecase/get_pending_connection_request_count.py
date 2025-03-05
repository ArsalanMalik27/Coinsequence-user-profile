from uuid import UUID

import structlog

from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)

logger = structlog.get_logger()


async def get_pending_connection_request_count_usecase(
    profile_id: UUID,
    connection_request_repo: ConnectionRequestRepository,
) -> int:
    return await connection_request_repo.get_pending_connection_request_count(
        profile_id
    )
