from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request

from app.container import Container
from app.domain.connections.data.connection_request import ConnectionRequestProps
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)
from app.domain.connections.usecase.get_connection_request_by_id import (
    get_connection_request_by_id_usecase,
)
from app.shared.utils.auth import AuthUser
from app.shared.utils.error import DomainError


@inject
async def valid_connection_request_id(
    connection_request_id: UUID,
    request: Request,
    connection_request_repo: ConnectionRequestRepository = Depends(
        Provide[Container.connection_request_db_repository]
    ),
) -> ConnectionRequestProps:
    user: AuthUser = request.state.user
    connection_request_props = await get_connection_request_by_id_usecase(
        connection_request_id, connection_request_repo
    )
    if not connection_request_props or connection_request_props.receiver.user_id != user.id:
        raise DomainError("Invalid Connection Request")
    return connection_request_props
