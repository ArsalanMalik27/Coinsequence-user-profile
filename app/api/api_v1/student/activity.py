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
from app.api.api_v1.student.dto.activity import (
    CreateActivityDTO,
    ActivityResponseDTO,
    UpdateActivityDTO
)
from app.api.api_v1.student.dependencies.profile import (
    other_profile_privacy,
    current_profile_privacy,
    other_profile_privacy_by_profile_id
)
from app.domain.student.data.profile_privacy import ProfilePrivacy, ProfileSectionType, ProfilePrivacyProps
from app.api.api_v1.connections.dependencies.connection import (
    get_connencted_profiles_count
)
from app.domain.connections.data.connection import ConnectionProps
from app.container import Container
from app.domain.student.usecase.create_activity import create_activity_usecase
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.usecase.update_activity import update_activity_usecase
from app.domain.student.usecase.delete_activity import delete_activity_usecase
from app.domain.student.usecase.get_activity_list import get_activity_list_usecase
from app.domain.student.usecase.get_other_activity_list import get_other_activity_list_usecase
from app.domain.student.data.activity import ActivityProps
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.activity import ActivityDBRepository
from app.repository.db.profile import UserProfileRepository
from app.repository.db.profile_privacy import ProfilePrivacyRepository
from app.repository.db.connection import ConnectionRepository
from app.shared.domain.data.page import Page

router = APIRouter()


@router.post("/", response_model=list[ActivityResponseDTO])
@inject
async def create_activity(
    create_activity_dto_list: list[CreateActivityDTO],
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    activity_repo: ActivityDBRepository = Depends(
        Provide[Container.activity_db_repository]
    ),
) -> list[ActivityProps]:
    activity_props_list = await create_activity_usecase(
        current_user_profile_props, create_activity_dto_list, activity_repo
    )
    return activity_props_list


@router.put("/", response_model=list[ActivityResponseDTO])
@inject
async def update_activity(
    update_activity_dto_list: list[UpdateActivityDTO],
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    activity_repo: ActivityDBRepository = Depends(
        Provide[Container.activity_db_repository]
    ),
) -> list[ActivityProps]:
    activity_props_list = await update_activity_usecase(
        update_activity_dto_list, activity_repo, current_user_profile_props
    )
    return activity_props_list



@router.delete("/{activity_id}")
@inject
async def delete_activity(
    activity_id: UUID,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    activity_repo: ActivityDBRepository = Depends(
        Provide[Container.activity_db_repository]
    ),
) -> str:
    await delete_activity_usecase(activity_id, current_user_profile_props, activity_repo)
    return "success"


@router.get("/",response_model=list[ActivityResponseDTO])
@inject
async def get_activity_list(
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    activity_repo: ActivityDBRepository = Depends(
        Provide[Container.activity_db_repository]
    )
) -> list[ActivityProps]:
    activity_list = await get_activity_list_usecase(current_user_profile_props, activity_repo)
    return activity_list

@router.get("/{profile_id}",response_model=list[ActivityResponseDTO])
@inject
async def get_activity_list(
    connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
    other_profile: UserProfileProps = Depends(other_profile_by_profile_id),
    profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy_by_profile_id),
    activity_repo: ActivityDBRepository = Depends(
        Provide[Container.activity_db_repository]
    ),
) -> list[ActivityProps]:
    activity_list = await get_other_activity_list_usecase(
        other_profile.id, activity_repo, profile_privacy_props, connected_profile)
    return activity_list