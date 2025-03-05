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
from app.api.api_v1.student.dto.voluntary import (
    CreateVoluntaryDTO,
    VoluntaryResponseDTO,
    UpdateVoluntaryDTO,
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
from app.domain.student.data.voluntary import VoluntaryProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.usecase.create_voluntary import create_voluntary_usecase
from app.domain.student.usecase.delete_voluntary import delete_voluntary_usecase
from app.domain.student.usecase.update_voluntary import update_voluntary_usecase
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.usecase.get_voluntary_list import get_voluntary_list_usecase
from app.domain.student.usecase.get_other_voluntary_list import get_other_voluntary_list_usecase
from app.repository.db.voluntary import VoluntaryDBRepository
from app.repository.db.profile import UserProfileRepository
from app.repository.db.profile_privacy import ProfilePrivacyRepository
from app.repository.db.connection import ConnectionRepository
from app.shared.domain.data.page import Page

router = APIRouter()


@router.post("/", response_model=VoluntaryResponseDTO)
@inject
async def create_voluntary(
    create_voluntary_dto: CreateVoluntaryDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    voluntary_repo: VoluntaryDBRepository = Depends(
        Provide[Container.voluntary_db_repository]
    ),
) -> VoluntaryProps:
    voluntary_props = await create_voluntary_usecase(
        current_user_profile_props, create_voluntary_dto, voluntary_repo
    )
    return voluntary_props


@router.put("/{voluntary_id}", response_model=VoluntaryResponseDTO)
@inject
async def update_voluntary(
    voluntary_id: UUID,
    update_voluntary_dto: UpdateVoluntaryDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    voluntary_repo: VoluntaryDBRepository = Depends(
        Provide[Container.voluntary_db_repository]
    ),
) -> VoluntaryProps:
    voluntary_props = await update_voluntary_usecase(
        voluntary_id, update_voluntary_dto, voluntary_repo, current_user_profile_props
    )
    return voluntary_props


@router.delete("/{voluntary_id}")
@inject
async def delete_voluntary_repo(
    voluntary_id: UUID,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    voluntary_repo:VoluntaryDBRepository = Depends(
        Provide[Container.voluntary_db_repository]
    ),
) -> str:
    await delete_voluntary_usecase(voluntary_id, current_user_profile_props, voluntary_repo)
    return "success"

@router.get("/")
@inject
async def get_voluntary_list(
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    voluntary_repo: VoluntaryDBRepository = Depends(
        Provide[Container.voluntary_db_repository]
    ),
) -> list:
    voluntary_list = await get_voluntary_list_usecase(current_user_profile_props, voluntary_repo)
    return voluntary_list

@router.get("/{profile_id}", response_model=list)
@inject
async def get_other_voluntary_list(
    other_profile: UserProfileProps = Depends(other_profile_by_profile_id),
    profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy_by_profile_id),
    connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
    voluntary_repo: VoluntaryDBRepository = Depends(
        Provide[Container.voluntary_db_repository]
    ),
) -> list:
    voluntary_list = await get_other_voluntary_list_usecase(
        other_profile.id, profile_privacy_props, connected_profile, voluntary_repo
    )
    return voluntary_list