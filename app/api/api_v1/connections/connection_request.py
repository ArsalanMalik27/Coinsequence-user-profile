from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.api.api_v1.connections.dependencies.connection_request import (
    valid_connection_request_id,
)
from app.api.api_v1.connections.dto.connection_request import (
    AcceptConnectionRequestResponseDTO,
    ConnectionsRequestParams,
    CreateConnectionRequestDTO,
    CreateConnectionRequestResponseDTO,
    RejectConnectionRequestResponseDTO,
)
from app.api.api_v1.student.dependencies.profile import valid_current_user_profile
from app.container import Container
from app.domain.connections.data.connection_request import ConnectionRequestProps
from app.domain.connections.repository.activity_stream import ActivityStream
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)
from app.domain.connections.usecase.create_connection_request import (
    create_connection_request_usecase,
)
from app.domain.connections.usecase.get_connection_requests import (
    get_connection_requests_usecase,
)
from app.domain.connections.usecase.update_connection_usecase import (
    accept_connection_request_usecase,
    reject_connection_request_usecase,
)
from app.domain.connections.usecase.withdraw_connection_request import (
    withdraw_connection_request_usecase,
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.shared.domain.data.page import Page
from app.shared.utils.auth import AuthUser
from app.domain.student.repository.db.children_profile import ChildrenProfileRepository

router = APIRouter()


@router.post("/", response_model=CreateConnectionRequestResponseDTO)
@inject
async def create_connection_request(
    create_connection_request_dto: CreateConnectionRequestDTO,
    request: Request,
    connection_request_repo: ConnectionRequestRepository = Depends(
        Provide[Container.connection_request_db_repository]
    ),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> ConnectionRequestProps:
    user: AuthUser = request.state.user
    user_profile = await get_user_profile_usecase(
        user.id, user_profile_repo
    )
    connection_request_props = await create_connection_request_usecase(
        user_profile.id, create_connection_request_dto, connection_request_repo
    )
    return connection_request_props


# {{url}}/connection-request/{{connectionRequestId}}/accept
@router.post(
    "/connection-request/{connection_request_id}/accept",
    response_model=AcceptConnectionRequestResponseDTO,
)
@inject
async def accept_connection_request(
    connection_request_props: ConnectionRequestProps = Depends(valid_connection_request_id),
    connection_request_repo: ConnectionRequestRepository = Depends(
        Provide[Container.connection_request_db_repository]
    ),
    connection_repo: ConnectionRepository = Depends(
        Provide[Container.connection_db_repository]
    ),
    activity_steam: ActivityStream = Depends(
        Provide[Container.getstream_activity_stream]
    ),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    children_profile_repo: ChildrenProfileRepository = Depends(
            Provide[Container.children_profile_db_repository]
        ),
) -> ConnectionRequestProps:
    return await accept_connection_request_usecase(
        connection_request_props, connection_request_repo, connection_repo, activity_steam, user_profile_repo,children_profile_repo
    )


@router.post(
    "/connection-request/{connectionRequestId}/reject",
    response_model=RejectConnectionRequestResponseDTO,
)
@inject
async def reject_connection_request(
    connectionRequestId: UUID,
    request: Request,
    connection_request_repo: ConnectionRequestRepository = Depends(
        Provide[Container.connection_request_db_repository]
    ),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> ConnectionRequestProps:
    user: AuthUser = request.state.user
    user_profile = await get_user_profile_usecase(
        user.id, user_profile_repo
    )
    print(user)
    connection_request_props = await reject_connection_request_usecase(
        connectionRequestId, connection_request_repo, user_profile.id
    )
    return connection_request_props


@router.get("/connection-request", response_model=dict)
@inject
async def list_connection_request(
    user_profile_props: UserProfileProps = Depends(valid_current_user_profile),
    connection_params: ConnectionsRequestParams = Depends(ConnectionsRequestParams),
    connection_request_repo: ConnectionRequestRepository = Depends(
        Provide[Container.connection_request_db_repository]
    ),
) -> Page[ConnectionRequestProps]:
    connection_requests_props = await get_connection_requests_usecase(
        user_profile_props, connection_request_repo, connection_params
    )
    return connection_requests_props


@router.delete("/connection-request/{connection_request_id}")
@inject
async def withdraw_connection_request(
    request: Request,
    connection_request_id: UUID,
    connection_request_repo: ConnectionRequestRepository = Depends(
        Provide[Container.connection_request_db_repository]
    ),
    userprofile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> str:
    user: AuthUser = request.state.user
    user_profile = await get_user_profile_usecase(user.id, userprofile_repo)
    await withdraw_connection_request_usecase(
        user_profile, connection_request_id, connection_request_repo
    )
    return "Success"
