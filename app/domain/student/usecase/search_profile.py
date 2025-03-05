from app.api.api_v1.student.dto.search_profile import SearchUsersParams
from app.domain.student.data.profile import UserProfileProps
from app.shared.domain.data.page import Page
from app.repository.db.profile import UserProfileRepository


async def search_student_profile_usecase(
    search_user_params: SearchUsersParams,
    user_profile_repo: UserProfileRepository,
    query: str | None
) -> Page[UserProfileProps]:
    return await user_profile_repo.get_searched_users(
        search_user_params.page,
        search_user_params.page_size,
        query,
        search_user_params
    )
