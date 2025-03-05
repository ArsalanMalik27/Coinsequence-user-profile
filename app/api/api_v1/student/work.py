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
from app.api.api_v1.student.dto.work import (
    CreateWorkDTO,
    WorkResponseDTO,
    UpdateWorkDTO
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
from app.domain.student.usecase.create_work import create_work_usecase
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.usecase.update_work import update_work_usecase
from app.domain.student.usecase.delete_work import delete_work_usecase
from app.domain.student.usecase.get_work_list import get_work_list_usecase
from app.domain.student.usecase.get_other_work_list import get_other_work_list_usecase
from app.domain.student.data.work import WorkProps
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.work import WorkDBRepository
from app.repository.db.profile import UserProfileRepository
from app.repository.db.profile_privacy import ProfilePrivacyRepository
from app.repository.db.connection import ConnectionRepository
from app.shared.domain.data.page import Page

router = APIRouter()


@router.post("/", response_model=WorkResponseDTO)
@inject
async def create_work(
    create_work_dto: CreateWorkDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    work_repo: WorkDBRepository = Depends(
        Provide[Container.work_db_repository]
    ),
) -> WorkProps:
    work_props = await create_work_usecase(
        current_user_profile_props, create_work_dto, work_repo
    )
    return work_props


@router.put("/", response_model=WorkResponseDTO)
@inject
async def update_work(
    work_id: UUID,
    update_work_dto: UpdateWorkDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    work_repo: WorkDBRepository = Depends(
        Provide[Container.work_db_repository]
    ),
) -> WorkProps:
    work_props = await update_work_usecase(
        work_id, update_work_dto, work_repo, current_user_profile_props
    )
    return work_props



@router.delete("/{work_id}")
@inject
async def delete_work(
    work_id: UUID,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    work_repo: WorkDBRepository = Depends(
        Provide[Container.work_db_repository]
    ),
) -> str:
    await delete_work_usecase(work_id, current_user_profile_props, work_repo)
    return "success"


@router.get("/",response_model=list[WorkProps])
@inject
async def get_work_list(
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    work_repo: WorkDBRepository = Depends(
        Provide[Container.work_db_repository]
    ),
) -> list[WorkProps]:
    work_list = await get_work_list_usecase(current_user_profile_props, work_repo)
    return work_list



@router.get("/{profile_id}", response_model=list[WorkProps])
@inject
async def get_other_work_list(
    work_repo: WorkDBRepository = Depends(
        Provide[Container.work_db_repository]
    ),
    connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
    other_profile: UserProfileProps = Depends(other_profile_by_profile_id),
    profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy_by_profile_id),

) -> list[WorkProps]:
    work_list = await get_other_work_list_usecase(
        other_profile.id, work_repo, profile_privacy_props, connected_profile
    )
    return work_list