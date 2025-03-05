from uuid import UUID

import structlog

from app.domain.student.data.education import EducationProps
from app.repository.db.education import EducationDBRepository

logger = structlog.get_logger()


async def get_education_by_id_usecase(
    education_id: UUID,
    education_repo: EducationDBRepository,
) -> EducationProps | None:
    education_props = await education_repo.get_by_id(
        education_id,
    )
    return education_props
