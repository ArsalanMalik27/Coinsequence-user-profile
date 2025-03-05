from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import Provide, inject
from app.api.api_v1.student.dto.application import ApplicationResponseDTO, CreateApplicationDTO
from app.container import Container
from app.repository.db.application import ApplicationDBRepository
from app.domain.student.data.application import CreateApplicationProps, ApplicationProps
from app.domain.student.usecase.create_application import create_application_usecase
from app.api.api_v1.student.dependencies.profile import (
    valid_student_profile_id,
    other_profile_by_profile_id,
)
from app.domain.student.usecase.list_all_application import list_all_application_usecase
from app.domain.student.data.profile import UserProfileProps
router = APIRouter()

@router.post("/me/application", response_model=ApplicationResponseDTO)
@inject
async def create_application(
    create_application_dto: CreateApplicationDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    application_repo: ApplicationDBRepository = Depends(
        Provide[Container.application_db_repository]
    ),
) -> ApplicationProps:
    application_props = await create_application_usecase(
        current_user_profile_props, create_application_dto, application_repo
    )
    return application_props

@router.get('/me/application', response_model=list[ApplicationResponseDTO])
@inject
async def get_application_list(
    current_user_profile_props: UserProfileProps = Depends(valid_student_profile_id),
    application_repo: ApplicationDBRepository = Depends(
        Provide[Container.application_db_repository]
    ),
) -> list[ApplicationProps]:
    application_props_list = await list_all_application_usecase(
        current_user_profile_props.id, application_repo
    )
    return application_props_list


@router.get('/{profile_id}/application', response_model=list[ApplicationResponseDTO])
@inject
async def get_others_application_list(
    other_profile: UserProfileProps = Depends(other_profile_by_profile_id),
    application_repo: ApplicationDBRepository = Depends(
        Provide[Container.application_db_repository]
    ),
) -> list[ApplicationProps]:
    application_props_list = await list_all_application_usecase(
        other_profile.id, application_repo
    )
    return application_props_list
