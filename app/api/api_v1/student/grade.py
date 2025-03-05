from typing import List
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.api.api_v1.student.dependencies.profile import (
    valid_current_user_profile,
    valid_student_profile_id,
    other_profile_by_profile_id
)
from app.api.api_v1.student.dto.grade import (
    CreateGradeDTO,
    GradeResponseDTO,
    UpdateGradeDTO,
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
from app.domain.student.data.grade import GradeProps
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.grade import GradeRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.repository.db.profile_privacy import ProfilePrivacyRepository
from app.repository.db.connection import ConnectionRepository
from app.domain.student.usecase.create_grade import create_grade_usecase
from app.domain.student.usecase.delete_grade import delete_grade_usecase
from app.domain.student.usecase.get_grade_list import get_grade_list_usecase
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.usecase.list_others_grades import list_others_grades_usecase
from app.domain.student.usecase.update_grade import update_grade_usecase
from app.shared.utils.auth import AuthUser

router = APIRouter()


@router.post("/", response_model=GradeResponseDTO)
@inject
async def create_grade(
    create_grade_dto: CreateGradeDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    grade_repo: GradeRepository = Depends(Provide[Container.grade_db_repository]),
) -> GradeProps:
    grade_props = await create_grade_usecase(
        create_grade_dto, grade_repo, current_user_profile_props
    )
    return grade_props


@router.put("/{grade_id}", response_model=GradeResponseDTO)
@inject
async def update_grade(
    grade_id: UUID,
    update_grade_dto: UpdateGradeDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    grade_repo: GradeRepository = Depends(Provide[Container.grade_db_repository]),
) -> GradeProps:
    grade_props = await update_grade_usecase(
        grade_id, update_grade_dto, grade_repo, current_user_profile_props
    )
    return grade_props


@router.delete("/{grade_id}")
@inject
async def delete_grade(
    grade_id: UUID,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    grade_repo: GradeRepository = Depends(Provide[Container.grade_db_repository]),
) -> str:
    await delete_grade_usecase(
        grade_id,
        grade_repo,
        current_user_profile_props,
    )
    return "success"


@router.get("/")
@inject
async def get_grades(
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    grade_repo: GradeRepository = Depends(Provide[Container.grade_db_repository]),
) -> list[GradeProps]:
    grade_list = await get_grade_list_usecase(
        grade_repo,
        current_user_profile_props,
    )
    return grade_list


@router.get("/{profile_id}", response_model=list[GradeResponseDTO])
@inject
async def list_others_grades(
    grade_repo: GradeRepository = Depends(
        Provide[Container.grade_db_repository]
    ),
    connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
    other_profile: UserProfileProps = Depends(other_profile_by_profile_id),
    profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy_by_profile_id),

) -> list[GradeProps]:
    grade_props = await list_others_grades_usecase(
        other_profile.id, grade_repo, profile_privacy_props, connected_profile
    )
    return grade_props