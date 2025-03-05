import structlog

from app.api.api_v1.student.dto.education import UpdateEducationDTO
from app.domain.student.data.education import (
    CreateEducationProps,
    Education,
    EducationProps,
)
from app.domain.student.data.profile import UserProfile, UserProfileProps
from app.domain.student.event.user_profile_updated import UserProfileUpdated
from app.domain.student.repository.db.education import EducationRepository
from app.infra.config import settings
from app.shared.repository.event_client import EventClient
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def update_education_usecase(
    education_props: EducationProps,
    current_user_profile_props: UserProfileProps,
    update_education_dto: UpdateEducationDTO,
    education_repo: EducationRepository,
    event_client: EventClient,
) -> EducationProps:
    if not update_education_dto.is_current and update_education_dto.start_date >= update_education_dto.end_date:
        raise DomainError("Invalid Date Range")
    if update_education_dto.is_current and not education_props.is_current:
        # Updating education to current
        await education_repo.update_is_current_by_profile_id(
            current_user_profile_props.id)
    education = Education(props=education_props)
    up_education_props = CreateEducationProps(**update_education_dto.dict())
    education.update_from(up_education_props)
    await education_repo.update_education(education.props)
    if education.props.is_current:
        user_profile = UserProfile(current_user_profile_props)
        user_profile.update_education(education.props)
        event = UserProfileUpdated.from_entity(user_profile.props)
        await event_client.publish(
            topic_name=settings.SNS.PROFILE_UPDATED, data=event
        )
    return education.props
