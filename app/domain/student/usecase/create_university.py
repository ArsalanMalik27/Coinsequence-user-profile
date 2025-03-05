import structlog

from app.api.api_v1.student.dto.college_university import CreateUniversityDTO
from app.domain.student.data.college_universities import (
    CreateUniversityProps,
    UniversityProps,University
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.college_university import UniversityRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.auth import AuthUser
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def create_university_usecase(
    userprofile_props: UserProfileProps,
    create_university_dto: CreateUniversityDTO,
    college_uni_repo: UniversityRepository,
) -> UniversityProps:
    if create_university_dto.start_date >= create_university_dto.end_date:
        raise DomainError("Invalid Date Range")
    
    universities_count = await college_uni_repo.universities_count_by_id(userprofile_props.id, create_university_dto.university_id)
    if universities_count >= 1:
        raise DomainError("University Already Exist")
    university_props = UniversityProps(**create_university_dto.dict())
    university = University.create_from(props=university_props, profile_id=userprofile_props.id)
    await college_uni_repo.create(university.props)
    return university.props