from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.api.api_v1.connections.dependencies.connection import (
    valid_connection_id_with_owner,
)
from app.api.api_v1.connections.dto.connection import ConnectionsParams
from app.api.api_v1.student.dependencies.profile import valid_current_user_profile
from app.container import Container
from app.domain.connections.data.connection import ConnectionProps
from app.domain.connections.repository.activity_stream import ActivityStream
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.connections.usecase.disconnect_connection import (
    disconnect_connection_usecase,
)
from app.domain.connections.usecase.get_connections import get_connections_usecase
from app.domain.student.data.profile import UserProfileProps
from app.shared.domain.data.page import Page

router = APIRouter()


@router.get("/", response_model=dict)
@inject
async def list_connections(
    current_user_profile_props: UserProfileProps = Depends(valid_current_user_profile),
    connection_repo: ConnectionRepository = Depends(
        Provide[Container.connection_db_repository]
    ),
    connection_params: ConnectionsParams = Depends(ConnectionsParams),
) -> Page[ConnectionProps]:
    list_connections_props = await get_connections_usecase(
        current_user_profile_props.id, connection_repo, connection_params
    )
    return list_connections_props

@router.delete("/{connection_id}")
@inject
async def disconnect_connection(
    connection_props: ConnectionProps =  Depends(valid_connection_id_with_owner),
    connection_repo: ConnectionRepository = Depends(
        Provide[Container.connection_db_repository]
    ),
    activity_steam: ActivityStream = Depends(
        Provide[Container.getstream_activity_stream]
    ),
) -> str:
    await disconnect_connection_usecase(
        connection_props, connection_repo, activity_steam
    )
    return "Success"
