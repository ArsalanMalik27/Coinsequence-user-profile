from fastapi.encoders import jsonable_encoder

from app.api.api_v1.student.dto.search_profile import SearchUsersParams
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.profile import UserProfileRepository
from app.shared.domain.data.page import Page
from app.shared.domain.repository.vectordb_client import VectorDBClient


async def search_student_profile_by_embeddings_usecase(
    vectordb_client: VectorDBClient,
    search_user_params: SearchUsersParams,
    user_profile_repo: UserProfileRepository,
    query: str | None
) -> Page[UserProfileProps]:

    json = jsonable_encoder(search_user_params)
    json['first_name'] = query
    json['last_name'] = query
    dataSet = str(json)

    result = vectordb_client.query(dataSet)

    ids = [item.id for item in result.matches]
    all_profiles = await user_profile_repo.get_all_by_user_ids(ids)

    return all_profiles
