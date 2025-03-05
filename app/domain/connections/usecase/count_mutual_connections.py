from uuid import UUID

from app.container import Container
from app.domain.connections.data.connection import ConnectionProps
from app.domain.connections.repository.db.connection import ConnectionRepository


async def count_mutual_connections_usecase(
    userprofile: UUID,
    other_profile: UUID,
    connection_repo: ConnectionRepository
) -> ConnectionProps:
    count = await connection_repo.count_mutual_connections(userprofile, other_profile)
    return count
