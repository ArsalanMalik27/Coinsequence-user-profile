from uuid import UUID

from app.container import Container
from app.domain.connections.data.connection import ConnectionProps
from app.domain.connections.repository.db.connection import ConnectionRepository


async def get_connection_usecase(
    profile_a_id: UUID,
    profile_b_id: UUID,
    connection_repo: ConnectionRepository
) -> ConnectionProps:
    connection_props = await connection_repo.get_by_profile_ids(profile_a_id, profile_b_id)
    return connection_props
