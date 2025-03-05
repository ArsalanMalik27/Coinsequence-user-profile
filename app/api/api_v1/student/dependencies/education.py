from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.container import Container
from app.domain.student.data.education import EducationProps
from app.domain.student.usecase.get_education_by_id import get_education_by_id_usecase
from app.repository.db.education import EducationDBRepository
from app.shared.utils.error import DomainError


@inject
async def valid_education_id(
    education_id: UUID,
    education_repo: EducationDBRepository = Depends(
        Provide[Container.education_db_repository]
    ),
) -> EducationProps:
    education_props = await get_education_by_id_usecase(
        education_id, education_repo
    )
    if not education_props:
        raise DomainError("Invalid Education Id")
    return education_props