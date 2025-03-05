from urllib.parse import parse_qs

import structlog
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.api.api_v1.student.dto.search_profile import (
    SearchUsersParams,
    SearchUsersQuery,
)
from app.container import Container
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.search_profile import (
    PAGE_QUERY_PARAMS,
    PROFILE_QUERY_PARAMS_MAPPING,
)
from app.domain.student.event.student_fund_courses import StudentFundCourseProps
from app.domain.student.repository.db.student_fund_courses import (
    StudentFundCoursesRepository,
)
from app.domain.student.usecase.handle_student_funds_courses_updated_event_usecase import (
    handle_student_funds_courses_updated_event_usecase,
)
from app.domain.student.usecase.search_profile import search_student_profile_usecase
from app.domain.student.usecase.search_profile_by_embeddings import (
    search_student_profile_by_embeddings_usecase,
)
from app.repository.db.profile import UserProfileRepository
from app.shared.domain.data.page import Page
from app.shared.domain.repository.vectordb_client import VectorDBClient

router = APIRouter()

logger = structlog.get_logger()


@router.get(
    "/fund/search/", response_model=dict
)
@inject
async def search_profile(
    request: Request,
    query: SearchUsersQuery = Depends(SearchUsersQuery),
    search_user_params: SearchUsersParams = Depends(SearchUsersParams),
    student_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    )
) -> Page[UserProfileProps]:
    # Filter out other query parameters
    errors = []
    allowed_params = PAGE_QUERY_PARAMS + tuple(
        item for row in PROFILE_QUERY_PARAMS_MAPPING.keys() for item in row
    )
    query_dict = parse_qs(str(request.query_params))
    extra = set(query_dict.keys()) - set(allowed_params)
    for param in extra:
        logger.info(
            f"search_profile: ignoring unknown query parameter, \"{param}\""
        )

    return await search_student_profile_usecase(
        search_user_params,
        student_profile_repo,
        query.query
    )


@router.get("/fund/search/embeddings")
@inject
async def search_profile_by_embeddings(
    request: Request,
    query: SearchUsersQuery = Depends(SearchUsersQuery),
    search_user_params: SearchUsersParams = Depends(SearchUsersParams),
    student_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    vectordb_client: VectorDBClient = Depends(
        Provide[Container.vectordb_client]
    ),
):
    allowed_params = PAGE_QUERY_PARAMS + tuple(
        item for row in PROFILE_QUERY_PARAMS_MAPPING.keys() for item in row
    )
    query_dict = parse_qs(str(request.query_params))
    extra = set(query_dict.keys()) - set(allowed_params)
    for param in extra:
        logger.info(
            f"search_profile_by_embeddings: ignoring unknown query parameter, \"{param}\""
        )
    return await search_student_profile_by_embeddings_usecase(
        vectordb_client,
        search_user_params,
        student_profile_repo,
        query.query,
    )
