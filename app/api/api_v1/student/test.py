from dependency_injector.wiring import Provide, inject
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import requests
from app.api.api_v1.student.dependencies.profile import (
    valid_current_user_profile,
    valid_student_profile_id,
    other_profile_by_profile_id
)
from app.api.api_v1.student.dto.score import (
    ScoreResponseDTO,
    UpdateScoreDTO,
    CreateScoreDTO,
)

from app.api.api_v1.student.dto.test import (
    TestResponseDTO,
    UpdateTestDTO,
    CreateTestDTO,
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
from app.domain.student.data.test import TestProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.usecase.create_test import create_test_usecase
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.usecase.create_udpate_test_score import create_update_test_score_usecase
from app.domain.student.usecase.list_others_test_score import list_others_test_score_usecase
from app.domain.student.usecase.list_test_score import list_test_score_usecase
from app.domain.student.usecase.delete_test import delete_test_usecase

from app.repository.db.score import ScoreDBRepository
from app.repository.db.test import TestDBRepository
from app.repository.db.profile_privacy import ProfilePrivacyRepository
from app.repository.db.connection import ConnectionRepository
from app.shared.utils.auth import AuthUser

from app.masterdata_shared.api_client import MasterdataAPIClient

router = APIRouter()


@router.post("/", response_model=TestResponseDTO)
@inject
async def create_test(
    create_test_dto: CreateTestDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    test_repo: TestDBRepository = Depends(Provide[Container.test_db_repository]),
) -> TestProps:
    test_props = await create_test_usecase(
        current_user_profile_props.id, create_test_dto, test_repo
    )
    return test_props


@router.post("/{test_id}/score", response_model=TestResponseDTO)
@inject
async def create_update_test_scores(
    test_id : UUID,
    update_score_dto_list: list[UpdateScoreDTO],
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    test_repo: TestDBRepository = Depends(Provide[Container.test_db_repository]),
    score_repo: ScoreDBRepository = Depends(Provide[Container.score_db_repository]),
    master_data_client: MasterdataAPIClient = Depends(Provide[Container.masterdata_client]),

) -> TestProps:
    test_props = await create_update_test_score_usecase(
        current_user_profile_props, test_id, update_score_dto_list, test_repo, score_repo,master_data_client
    )
    return test_props

@router.get("/{profile_id}", response_model=list[TestProps])
@inject
async def list_others_test_scores(
    connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
    other_profile: UserProfileProps = Depends(other_profile_by_profile_id),
    profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy_by_profile_id),
    test_repo: TestDBRepository = Depends(Provide[Container.test_db_repository]),
) -> list[TestProps]:
    test_score_props_list = await list_others_test_score_usecase(
        other_profile.id, test_repo, profile_privacy_props, connected_profile)
    return test_score_props_list

@router.get("/", response_model=list[TestProps])
@inject
async def list_test_scores(
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    test_repo: TestDBRepository = Depends(Provide[Container.test_db_repository]),
) -> list[TestProps]:
    test_score_props_list = await list_test_score_usecase(
        current_user_profile_props,
        test_repo
    )
    return test_score_props_list

@router.delete("/{test_id}")
@inject
async def delete_test(
    test_id: UUID,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    test_repo: TestDBRepository = Depends(Provide[Container.test_db_repository]),
) -> str:
    await delete_test_usecase(
        current_user_profile_props.id, test_id, test_repo
    )
    return "Success"