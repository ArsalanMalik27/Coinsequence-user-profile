from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.api_v1.connections.dependencies.connection import (
    get_connencted_profiles_count,
)
from app.api.api_v1.student.dependencies.education import valid_education_id
from app.api.api_v1.student.dependencies.profile import (
    other_profile_by_profile_id,
    other_profile_privacy_by_profile_id,
    valid_student_or_teacher_profile_id,
)
from app.api.api_v1.student.dto.education import (
    CreateEducationDTO,
    EducationResponseDTO,
    UpdateEducationDTO,
)
from app.container import Container
from app.domain.connections.data.connection import ConnectionProps
from app.domain.student.data.education import EducationProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacyProps
from app.domain.student.usecase.create_education import create_education_usecase
from app.domain.student.usecase.delete_education import delete_education_usecase
from app.domain.student.usecase.list_all_education import list_all_education_usecase
from app.domain.student.usecase.list_others_education import (
    list_others_education_usecase,
)
from app.domain.student.usecase.update_education import update_education_usecase
from app.repository.db.education import EducationDBRepository
from app.shared.domain.repository.event_client import EventClient
from app.shared.utils.error import DomainError

router = APIRouter()


@router.post("/", response_model=EducationResponseDTO)
@inject
async def create_education(
    create_education_dto: CreateEducationDTO,
    current_user_profile_props: UserProfileProps = Depends(
        valid_student_or_teacher_profile_id
    ),
    education_repo: EducationDBRepository = Depends(
        Provide[Container.education_db_repository]
    ),
    event_client: EventClient = Depends(Provide[Container.event_client]),
) -> EducationProps:
    education_props = await create_education_usecase(
        current_user_profile_props, create_education_dto, education_repo, event_client
    )
    return education_props


@router.put("/{education_id}", response_model=EducationResponseDTO)
@inject
async def update_education(
    update_education_dto: UpdateEducationDTO,
    current_user_profile_props: UserProfileProps = Depends(
        valid_student_or_teacher_profile_id
    ),
    education_props: EducationProps = Depends(valid_education_id),
    education_repo: EducationDBRepository = Depends(
        Provide[Container.education_db_repository]
    ),
    event_client: EventClient = Depends(Provide[Container.event_client]),
) -> EducationProps:
    if education_props.profile_id != current_user_profile_props.id:
        raise DomainError("Invalid Education")
    education_props = await update_education_usecase(
        education_props,
        current_user_profile_props,
        update_education_dto,
        education_repo,
        event_client,
    )
    return education_props


@router.delete("/{education_id}")
@inject
async def delete_education(
    education_id: UUID,
    current_user_profile_props: UserProfileProps = Depends(
        valid_student_or_teacher_profile_id
    ),
    education_repo: EducationDBRepository = Depends(
        Provide[Container.education_db_repository]
    ),
) -> str:
    await delete_education_usecase(
        education_id, current_user_profile_props, education_repo
    )
    return "success"


@router.get("/", response_model=list)
@inject
async def list_all_educations(
    current_user_profile_props: UserProfileProps = Depends(
        valid_student_or_teacher_profile_id
    ),
    education_repo: EducationDBRepository = Depends(
        Provide[Container.education_db_repository]
    ),
) -> list[EducationProps]:
    education_props = await list_all_education_usecase(
        current_user_profile_props,
        education_repo,
    )
    return education_props


@router.get("/{profile_id}", response_model=list)
@inject
async def list_others_educations(
    education_repo: EducationDBRepository = Depends(
        Provide[Container.education_db_repository]
    ),
    connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
    other_profile: UserProfileProps = Depends(other_profile_by_profile_id),
    profile_privacy_props: ProfilePrivacyProps = Depends(
        other_profile_privacy_by_profile_id
    ),
) -> list[EducationProps]:
    education_props = await list_others_education_usecase(
        other_profile.id, education_repo, connected_profile, profile_privacy_props
    )
    return education_props
