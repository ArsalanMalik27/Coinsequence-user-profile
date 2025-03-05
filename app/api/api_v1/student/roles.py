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
from app.api.api_v1.student.dto.roles import (
    CreateRolesDTO,
    RolesResponseDTO,
    UpdateRolesDTO,
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
from app.domain.student.data.roles import RolesProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.usecase.create_roles import create_roles_usecase
from app.domain.student.usecase.delete_roles import delete_roles_usecase
from app.domain.student.usecase.update_roles import update_roles_usecase
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.usecase.get_roles_list import get_roles_list_usecase
from app.domain.student.usecase.get_other_roles_list import get_others_roles_list_usecase
from app.repository.db.roles import RolesDBRepository
from app.repository.db.profile import UserProfileRepository
from app.repository.db.profile_privacy import ProfilePrivacyRepository
from app.repository.db.connection import ConnectionRepository
from app.shared.domain.data.page import Page

router = APIRouter()


@router.post("/", response_model=RolesResponseDTO)
@inject
async def create_roles(
    create_roles_dto: CreateRolesDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    roles_repo: RolesDBRepository = Depends(
        Provide[Container.roles_db_repository]
    ),
) -> RolesProps:
    roles_props = await create_roles_usecase(
        current_user_profile_props, create_roles_dto, roles_repo
    )
    return roles_props


@router.put("/", response_model=RolesResponseDTO)
@inject
async def update_roles(
    roles_id: UUID,
    update_roles_dto: UpdateRolesDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    roles_repo: RolesDBRepository = Depends(
        Provide[Container.roles_db_repository]
    ),
) -> RolesProps:
    roles_props = await update_roles_usecase(
        roles_id, update_roles_dto, roles_repo, current_user_profile_props
    )
    return roles_props


@router.delete("/{roles_id}")
@inject
async def delete_roles(
    roles_id: UUID,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    roles_repo: RolesDBRepository = Depends(
        Provide[Container.roles_db_repository]
    ),
) -> str:
    await delete_roles_usecase(roles_id, current_user_profile_props, roles_repo)
    return "success"

@router.get("/")
@inject
async def get_roles_list(
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    roles_repo: RolesDBRepository = Depends(
        Provide[Container.roles_db_repository]
    ),
) -> list:
    roles_list = await get_roles_list_usecase(current_user_profile_props, roles_repo)
    return roles_list

@router.get("/{profile_id}")
@inject
async def get_other_roles_list(
    roles_repo: RolesDBRepository = Depends(
        Provide[Container.roles_db_repository]
    ),
    connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
    other_profile: UserProfileProps = Depends(other_profile_by_profile_id),
    profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy_by_profile_id),

) -> list:
    roles_list = await get_others_roles_list_usecase(
        other_profile.id, roles_repo, profile_privacy_props, connected_profile)
    return roles_list