from uuid import UUID

import structlog

from app.domain.connections.data.connection_request import ConnectionRequestProps
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def get_connection_request_by_id_usecase(
    id: UUID,
    connection_request_repo: ConnectionRequestRepository,
) -> ConnectionRequestProps | None:
    connection_request_props = (
        await connection_request_repo.get_pending_by_id(id)
    )
    if not connection_request_props:
        raise DomainError("Invalid Connection Request ID")
    return connection_request_props
