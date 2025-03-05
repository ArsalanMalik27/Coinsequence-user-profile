from uuid import UUID

import structlog
from typing import List, Optional

from app.api.api_v1.student.dto.grade import GradeListParams

from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.grade import GradeProps
from app.domain.student.repository.db.grade import GradeRepository
from app.shared.domain.data.page import Page
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def get_grade_list_usecase(
    grade_repo: GradeRepository,
    profile_props: UserProfileProps,
) -> List[Optional[GradeProps]]:
    grade_props_list = await grade_repo.grade_list(profile_props.id)
    return grade_props_list
