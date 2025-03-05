from uuid import UUID

import structlog

from app.api.api_v1.connections.dto.connection_request import CreateConnectionRequestDTO
from app.domain.connections.data.connection_request import (
    ConnectionRequest,
    ConnectionRequestProps,
    ConnectionRequestStatus,
)
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def create_connection_request_usecase(
    profile_id: UUID,
    create_connection_request_dto: CreateConnectionRequestDTO,
    connection_request_repo: ConnectionRequestRepository,
) -> ConnectionRequestProps:
    connection_request_props = await connection_request_repo.get_by_profile_ids(
        profile_id,
        create_connection_request_dto.receiver_id,
        ConnectionRequestStatus.PENDING
    )
    if connection_request_props:
        raise DomainError("Already requested for this connection.")
    connection_request = ConnectionRequest.from_create_props(
        create_connection_request_dto, profile_id
    )
    await connection_request_repo.create_connection_request(connection_request.props)
    return connection_request.props
