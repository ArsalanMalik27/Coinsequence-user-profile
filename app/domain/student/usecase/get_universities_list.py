import structlog

from app.api.api_v1.student.dto.award import CreateAwardDTO
from app.domain.student.data.award import (
    CreateAwardProps,
    AwardProps,
    Award
)
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.college_university import UniversityDBRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.auth import AuthUser

logger = structlog.get_logger()

async def get_universities_list_usecase(
    profile_props: UserProfileProps,
    university_repo: UniversityDBRepository
)->list:
    universities_list = await university_repo.get_all_universities(profile_props.id)
    return universities_list
