from uuid import UUID

import structlog

from app.domain.connections.data.connection import ConnectionProps
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def get_connection_by_id_usecase(
    id: UUID,
    connection_repo: ConnectionRepository,
) -> ConnectionProps | None:
    connection_props = await connection_repo.get_connection_by_id(id)
    if not connection_props:
        raise DomainError("Invalid Connection ID")
    return connection_props
