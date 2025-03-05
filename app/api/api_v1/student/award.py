from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.api_v1.student.dependencies.profile import (
    valid_current_user_profile,
    valid_student_profile_id,
    other_profile_by_profile_id
)
from app.api.api_v1.student.dto.award import (
    CreateAwardDTO,
    AwardResponseDTO,
    UpdateAwardDTO
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
from app.domain.student.usecase.create_award import create_award_usecase
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.usecase.update_award import update_award_usecase
from app.domain.student.usecase.delete_award import delete_award_usecase
from app.domain.student.usecase.get_award_list import get_award_list_usecase
from app.domain.student.usecase.get_other_award_list import get_other_award_list_usecase
from app.domain.student.data.award import AwardProps
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.award import AwardDBRepository
from app.repository.db.profile import UserProfileRepository
from app.repository.db.profile_privacy import ProfilePrivacyRepository
from app.repository.db.connection import ConnectionRepository
from app.shared.domain.data.page import Page

router = APIRouter()


@router.post("/", response_model=AwardResponseDTO)
@inject
async def create_award(
    create_award_dto: CreateAwardDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    award_repo: AwardDBRepository = Depends(
        Provide[Container.award_db_repository]
    ),
) -> AwardProps:
    award_props = await create_award_usecase(
        current_user_profile_props, create_award_dto, award_repo
    )
    return award_props


@router.put("/", response_model=AwardResponseDTO)
@inject
async def update_award(
    award_id: UUID,
    update_award_dto: UpdateAwardDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    award_repo: AwardDBRepository = Depends(
        Provide[Container.award_db_repository]
    ),
) -> AwardProps:
    award_props = await update_award_usecase(
        award_id, update_award_dto, award_repo, current_user_profile_props
    )
    return award_props



@router.delete("/{award_id}")
@inject
async def delete_award(
    award_id: UUID,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    award_repo: AwardDBRepository = Depends(
        Provide[Container.award_db_repository]
    ),
) -> str:
    await delete_award_usecase(award_id, current_user_profile_props, award_repo)
    return "success"


@router.get("/",response_model=list[AwardResponseDTO])
@inject
async def get_award_list(
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    award_repo: AwardDBRepository = Depends(
        Provide[Container.award_db_repository]
    ),
) -> list[AwardProps]:
    award_list = await get_award_list_usecase(current_user_profile_props, award_repo)
    return award_list

@router.get("/{profile_id}",response_model=list[AwardResponseDTO])
@inject
async def get_other_award_list(
    award_repo: AwardDBRepository = Depends(
        Provide[Container.award_db_repository]
    ),
    connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
    other_profile: UserProfileProps = Depends(other_profile_by_profile_id),
    profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy_by_profile_id),
) -> list[AwardProps]:
    award_list = await get_other_award_list_usecase(
        other_profile.id, award_repo, profile_privacy_props, connected_profile
    )
    return award_list