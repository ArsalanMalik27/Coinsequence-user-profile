from uuid import UUID

import structlog

from app.domain.connections.data.connection_request import (
    ConnectionRequest,
    ConnectionRequestProps,
)
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)
from app.domain.student.data.profile import UserProfileProps
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def withdraw_connection_request_usecase(
        user_profile: UserProfileProps,
        connection_request_id: UUID,
        connection_request_repo: ConnectionRequestRepository,
)->None:
    connection_request = await connection_request_repo.get_pending_by_id(connection_request_id)
    if not connection_request or connection_request.sender_id != user_profile.id:
        raise DomainError("Invalid Connection Request")
    await connection_request_repo.delete(connection_request_id)
