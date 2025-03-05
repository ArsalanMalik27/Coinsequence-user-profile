from fastapi import Query

from app.domain.connections.data.connection_request import (
    ConnectionRequestProps,
    ConnectionRequestStatus,
    CreateConnectionRequestProps,
)
from app.shared.domain.data.page import PageRequestDTO


class CreateConnectionRequestDTO(CreateConnectionRequestProps):
    pass


class CreateConnectionRequestResponseDTO(ConnectionRequestProps):
    pass


class AcceptConnectionRequestDTO(ConnectionRequestProps):
    pass


class AcceptConnectionRequestResponseDTO(ConnectionRequestProps):
    pass


class RejectConnectionRequestDTO(ConnectionRequestProps):
    pass


class RejectConnectionRequestResponseDTO(ConnectionRequestProps):
    pass


class GetConnectionRequestDTO:
    pass


class GetConnectionRequestResponseDTO(ConnectionRequestProps):
    pass


class ConnectionsRequestParams(PageRequestDTO):
    status: ConnectionRequestStatus | None = None
    query: str = Query(default="", title="query")
