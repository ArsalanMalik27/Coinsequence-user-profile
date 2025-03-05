from uuid import UUID
import structlog

from app.api.api_v1.student.dto.college_university import CreateUniversityDTO,UpdateUniversityDTO
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


async def update_university_usecase(
    university_id: UUID,
    update_university_dto: UpdateUniversityDTO,
    university_repo: UniversityRepository,
    user_profile_props: UserProfileProps,
) -> CreateUniversityProps:
    if update_university_dto.start_date >= update_university_dto.end_date:
        raise DomainError("Invalid Date Range")
    universities_count = await university_repo.universities_count_by_id(user_profile_props.id, update_university_dto.university_id)
    if universities_count > 1:
        raise DomainError("University Already Exist")
    existing_university = await university_repo.get_by_id(university_id)
    if not existing_university or existing_university.profile_id != user_profile_props.id:
        logger.info(
            "[UpdateUniversityUsecase: attempt to update non-existing University]",
            data=user_profile_props,
        )
        raise DomainError("Invalid University")
    print(existing_university)
    upgrade_university_props = UniversityProps(**update_university_dto.dict())
    university_props = University(props=existing_university)
    university_props.update_from(upgrade_university_props)
    await university_repo.update_university(university_props.props, user_profile_props.id)
    return university_props.props
