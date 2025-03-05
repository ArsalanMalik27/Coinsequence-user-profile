from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.domain.repository.vectordb_client import VectorDBClient


async def upsert_profile_embedding_usecase(
    user_id: UUID,
    user_profile_repo: UserProfileRepository,
    vectordb_client: VectorDBClient
):
    result = await user_profile_repo.get_all_joined_by_user_id(user_id)
    dataSet = str(jsonable_encoder(result))
    metadata = {
        "user_id": str(user_id),
        "user_data": dataSet,
    }

    vectordb_client.upsert(str(user_id), dataSet, metadata)

    return dataSet
