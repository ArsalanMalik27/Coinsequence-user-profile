import structlog

from app.domain.connections.data.connection import ConnectionProps
from app.domain.connections.repository.activity_stream import ActivityStream
from app.domain.connections.repository.db.connection import ConnectionRepository

logger = structlog.get_logger()


async def disconnect_connection_usecase(
    connection_props: ConnectionProps,
    connection_repo: ConnectionRepository,
    activity_steam: ActivityStream
) -> None:
    await connection_repo.delete(connection_props.id)
    activity_steam.unfollow(str(connection_props.user_a_profile.user_id), str(connection_props.user_b_profile.user_id))
    activity_steam.unfollow(str(connection_props.user_b_profile.user_id), str(connection_props.user_a_profile.user_id))
