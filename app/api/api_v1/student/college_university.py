from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.shared.utils.auth import AuthUser

from app.api.api_v1.student.dependencies.profile import (
    valid_current_user_profile,
    valid_student_profile_id,
    other_profile_by_profile_id
)
from app.api.api_v1.student.dto.college_university import (
    CreateUniversityDTO,
    UniversityResponseDTO,
    UpdateUniversityDTO,
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
from app.domain.student.data.college_universities import UniversityProps,CreateUniversityProps
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.college_university import UniversityDBRepository
from app.repository.db.profile import UserProfileRepository
from app.repository.db.profile_privacy import ProfilePrivacyRepository
from app.repository.db.connection import ConnectionRepository
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.usecase.create_university import create_university_usecase
from app.domain.student.usecase.update_university import update_university_usecase
from app.domain.student.usecase.delete_university import delete_university_usecase
from app.domain.student.usecase.get_universities_list import get_universities_list_usecase
from app.domain.student.usecase.get_other_universities_list import get_other_universities_list_usecase


router = APIRouter()


@router.post("/", response_model=UniversityResponseDTO)
@inject
async def create_college_university(
    create_university_dto: CreateUniversityDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    university_repo: UniversityDBRepository = Depends(
        Provide[Container.university_db_repository]
    ),
) -> None:
    university_props = await create_university_usecase(
        current_user_profile_props, create_university_dto, university_repo
    )
    return university_props


@router.put("/", response_model=UniversityResponseDTO)
@inject
async def update_univeristy(
    university_id: UUID,
    update_university_dto: UpdateUniversityDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    university_repo: UniversityDBRepository = Depends(
        Provide[Container.university_db_repository]
    ),
) -> CreateUniversityProps:
    university_props = await update_university_usecase(
        university_id, update_university_dto, university_repo, current_user_profile_props
    )
    return university_props


@router.delete("/{university_id}")
@inject
async def delete_university(
    university_id: UUID,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    university_repo: UniversityDBRepository = Depends(
        Provide[Container.university_db_repository]
    ),
) -> str:
    await delete_university_usecase(university_id, current_user_profile_props, university_repo)
    return "success"


@router.get("/")
@inject
async def get_university_list(
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    university_repo: UniversityDBRepository = Depends(
        Provide[Container.university_db_repository]
    ),
) -> list:
    universities_list = await get_universities_list_usecase(current_user_profile_props, university_repo)
    return universities_list

@router.get("/{profile_id}")
@inject
async def get_other_university_list(
    university_repo: UniversityDBRepository = Depends(
        Provide[Container.university_db_repository]
    ),
    connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
    other_profile: UserProfileProps = Depends(other_profile_by_profile_id),
    profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy_by_profile_id),

) -> list:
    universities_list = await get_other_universities_list_usecase(
        other_profile.id, university_repo, profile_privacy_props, connected_profile)
    return universities_list