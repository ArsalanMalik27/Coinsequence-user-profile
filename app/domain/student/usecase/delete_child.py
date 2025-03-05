from uuid import UUID
import structlog

from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.children_profile import ChildrenProfileRepository
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.connections.repository.activity_stream import ActivityStream
from app.domain.connections.usecase.disconnect_connection import disconnect_connection_usecase
from app.shared.utils.error import DomainError
from app.shared.utils.auth import AuthUser

logger = structlog.get_logger()


async def delete_child_usecase(
    child_id: UUID,
    profile_props: UserProfileProps,
    children_profile_repo: ChildrenProfileRepository,
    connection_repo: ConnectionRepository,
    activity_steam: ActivityStream
) -> None:
    child_props = await children_profile_repo.get_by_profile_ids(child_id,profile_props.id)
    if not child_props or profile_props.id != child_props.parent_id:
        raise DomainError("Invalid Child")
    connection_props = await connection_repo.get_by_profile_ids(child_id, profile_props.id)
    if not connection_props:
        raise DomainError("Invalid Connection with Child")
    await children_profile_repo.delete(child_props.id)
    await disconnect_connection_usecase(
        connection_props,connection_repo,activity_steam
    )

