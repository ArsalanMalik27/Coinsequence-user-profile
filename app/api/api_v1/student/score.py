from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.api.api_v1.student.dto.score import (
    CreateScoreDTO,
    ScoreResponseDTO,
    UpdateScoreDTO,
)
from app.api.api_v1.student.dependencies.profile import (
    other_profile_privacy,
    current_profile_privacy,
    other_profile_privacy_by_profile_id
)
from app.api.api_v1.connections.dependencies.connection import (
    get_connencted_profiles_count
)
from app.domain.connections.data.connection import ConnectionProps
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType, ProfilePrivacyProps
from app.container import Container
from app.domain.student.data.score import ScoreProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.usecase.create_score import create_score_usecase
from app.domain.student.usecase.delete_score import delete_score_usecase
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.usecase.get_score import get_score_usecase
from app.domain.student.usecase.list_others_score import list_others_score_usecase
from app.domain.student.usecase.update_score import update_score_usecase
from app.repository.db.score import ScoreDBRepository
from app.shared.utils.auth import AuthUser

router = APIRouter()


@router.post("/", response_model=ScoreResponseDTO)
@inject
async def create_score(
    request: Request,
    create_score_dto: CreateScoreDTO,
    score_repo: ScoreDBRepository = Depends(Provide[Container.score_db_repository]),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository],
    ),
) -> ScoreProps:
    user: AuthUser = request.state.user
    userprofile = await get_user_profile_usecase(user.id, user_profile_repo)
    score_props = await create_score_usecase(
        userprofile.id, create_score_dto, score_repo
    )
    return score_props


@router.put("/{score_id}", response_model=ScoreResponseDTO)
@inject
async def update_score(
    request: Request,
    score_id: UUID,
    update_score_dto: UpdateScoreDTO,
    score_repo: ScoreDBRepository = Depends(Provide[Container.score_db_repository]),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> ScoreProps:
    user: AuthUser = request.state.user
    userprofile = await get_user_profile_usecase(
        user.id,
        user_profile_repo,
    )
    score_props = await update_score_usecase(
        userprofile.id, score_id, update_score_dto, score_repo
    )
    return score_props


@router.get("/", response_model=list[ScoreProps])
@inject
async def get_score(
    request: Request,
    score_repo: ScoreDBRepository = Depends(Provide[Container.score_db_repository]),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> list[ScoreProps]:
    user: AuthUser = request.state.user
    userprofile = await get_user_profile_usecase(
        user.id,
        user_profile_repo,
    )
    score_list = await get_score_usecase(userprofile.id, score_repo)
    return score_list


@router.delete("/{score_id}")
@inject
async def delete_score(
    request: Request,
    score_id: UUID,
    score_repo: ScoreDBRepository = Depends(Provide[Container.score_db_repository]),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> str:
    user: AuthUser = request.state.user
    userprofile = await get_user_profile_usecase(
        user.id,
        user_profile_repo,
    )
    await delete_score_usecase(
        userprofile.id,
        score_id,
        score_repo,
    )
    return "Success"

@router.get("/{profile_id}", response_model=list[ScoreProps])
@inject
async def list_others_scores(
    profile_id: UUID,
    connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
    profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy_by_profile_id),
    score_repo: ScoreDBRepository = Depends(
        Provide[Container.score_db_repository]
    ),
) -> list[ScoreProps]:
    score_props = await list_others_score_usecase(
        profile_id, profile_privacy_props, connected_profile, score_repo
    )
    return score_props