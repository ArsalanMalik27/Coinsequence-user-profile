from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request

from app.container import Container
from app.domain.connections.data.connection_request import ConnectionRequestProps
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.connections.usecase.get_connection_by_id import (
    get_connection_by_id_usecase,
)
from app.shared.utils.auth import AuthUser
from app.shared.utils.error import DomainError

from app.domain.connections.data.connection import ConnectionProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.data.profile import UserProfileProps, UserProfileType

@inject
async def valid_connection_id_with_owner(
    connection_id: UUID,
    request: Request,
    connection_repo: ConnectionRepository = Depends(
        Provide[Container.connection_db_repository]
    ),
) -> ConnectionRequestProps:
    user: AuthUser = request.state.user
    connection__props = await get_connection_by_id_usecase(
        connection_id, connection_repo
    )
    if not connection__props or (connection__props.user_a_profile.user_id != user.id and connection__props.user_b_profile.user_id != user.id):
        raise DomainError("Invalid Connection")
    return connection__props


@inject
async def get_connencted_profiles_count(
    request: Request,
    profile_id: UUID,
    connection_repo: ConnectionRepository = Depends(
        Provide[Container.connection_db_repository]
    ),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> int:
    user: AuthUser = request.state.user
    current_user_profile = await get_user_profile_usecase(
        user.id, user_profile_repo
    )
    connected_profiles = await connection_repo.get_connected_user(user_a=current_user_profile.id, user_b=profile_id)
    return connected_profiles


@inject
async def get_connection(
    request: Request,
    user_id: UUID,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    connection_repo: ConnectionRepository = Depends(
        Provide[Container.connection_db_repository]
    ),
) -> ConnectionProps:
    user: AuthUser = request.state.user
    current_profile_props = await get_user_profile_usecase(
        user.id, user_profile_repo
    )
    if not current_profile_props:
        raise DomainError("Profile doesn't exist")
    other_profile_props = await get_user_profile_usecase(
        user_id, user_profile_repo
    )
    if not other_profile_props:
        raise DomainError("Invalid Profile Id")
    connection_props = await connection_repo.get_by_profile_ids(current_profile_props.id, other_profile_props.id)
    return connection_props


@inject
async def get_connection_by_profile_id(
    request: Request,
    profile_id: UUID,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    connection_repo: ConnectionRepository = Depends(
        Provide[Container.connection_db_repository]
    ),
) -> ConnectionProps:
    user: AuthUser = request.state.user
    current_profile_props = await get_user_profile_usecase(
        user.id, user_profile_repo
    )
    if not current_profile_props:
        raise DomainError("Profile doesn't exist")

    connection_props = await connection_repo.get_by_profile_ids(current_profile_props.id, profile_id)
    return connection_props