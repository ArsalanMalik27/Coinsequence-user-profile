from uuid import UUID

import structlog

from app.domain.connections.data.connection import Connection, ConnectionProps
from app.domain.student.data.profile import UserProfileProps, UserProfile
from app.domain.connections.data.connection_request import (
    ConnectionRequest,
    ConnectionRequestProps,
)
from app.domain.student.data.children_profile import Children_Profile,ChildrenProfileProps

from app.domain.connections.repository.activity_stream import ActivityStream
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)
from app.domain.student.repository.db.children_profile import ChildrenProfileRepository
from app.domain.student.data.profile import UserProfileType
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def accept_connection_request_usecase(
    connection_request_props: ConnectionRequestProps,
    connection_request_repo: ConnectionRequestRepository,
    connection_repo: ConnectionRepository,
    activity_steam: ActivityStream,
    user_profile_repo: UserProfileRepository,
    children_profile_repo: ChildrenProfileRepository,

) -> ConnectionRequestProps | None:
    connection_request = ConnectionRequest(connection_request_props)
    connection_request.accept()
    if connection_request.props.sender.profile_type == UserProfileType.PARENT:
        connection_request.is_parent()
        child_props = await children_profile_repo.get_by_profile_ids(connection_request.props.receiver_id,connection_request.props.sender_id)
        child_profile = Children_Profile(props=child_props)
        child_profile_props = child_profile.update_confirmation()
        await children_profile_repo.update(child_profile_props.props)
    await connection_request_repo.update_connection_request(connection_request.props)
    connection = Connection.from_users(
        connection_request.props.sender_id,
        connection_request.props.receiver_id,
        connection_request.props.is_parent
    )
    await connection_repo.create_connection(connection.props)
    activity_steam.follow(str(connection_request_props.sender.user_id), str(connection_request_props.receiver.user_id))
    activity_steam.follow(str(connection_request_props.receiver.user_id), str(connection_request_props.sender.user_id))

    sender_profile_props = await user_profile_repo.get_by_user_id(connection_request_props.sender.user_id)
    sender_profile = UserProfile(props=sender_profile_props)
    sender_con_count = await connection_repo.get_connection_count(sender_profile.props.id)
    sender_profile.update_connection_count(sender_con_count)
    await user_profile_repo.update_profile(sender_profile.props)

    receiver_profile_props = await user_profile_repo.get_by_user_id(connection_request_props.receiver.user_id)
    receiver_profile = UserProfile(props=receiver_profile_props)
    receiver_con_count = await connection_repo.get_connection_count(receiver_profile.props.id)
    receiver_profile.update_connection_count(receiver_con_count)
    await user_profile_repo.update_profile(receiver_profile.props)

    return connection_request.props


async def reject_connection_request_usecase(
    id: UUID,
    connection_request_repo: ConnectionRequestRepository,
    profile_id: UUID,
) -> ConnectionRequestProps | None:
    connection_request_props = (
        await connection_request_repo.get_pending_by_id(id)
    )
    if not connection_request_props or connection_request_props.receiver_id != profile_id:
        raise DomainError("Invalid Connection Request")
    connection_request = ConnectionRequest.from_connection_request_props(
        connection_request_props
    )
    connection_request.reject()
    await connection_request_repo.update_connection_request(connection_request.props)
    return connection_request.props
