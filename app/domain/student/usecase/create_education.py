import structlog

from app.api.api_v1.student.dto.education import CreateEducationDTO
from app.domain.student.data.education import (
    CreateEducationProps,
    Education,
    EducationProps,
)
from app.domain.student.data.profile import UserProfile, UserProfileProps
from app.domain.student.event.user_profile_updated import UserProfileUpdated
from app.domain.student.repository.db.education import EducationRepository
from app.infra.config import settings
from app.shared.domain.repository.event_client import EventClient
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def create_education_usecase(
    current_user_profile_props: UserProfileProps,
    create_education_dto: CreateEducationDTO,
    education_repo: EducationRepository,
    event_client: EventClient,
) -> EducationProps:
    if (
        not create_education_dto.is_current
        and create_education_dto.start_date >= create_education_dto.end_date
    ):
        raise DomainError("Invalid Date Range")
    if create_education_dto.is_current:
        await education_repo.update_is_current_by_profile_id(
            current_user_profile_props.id
        )
    education_props = CreateEducationProps(**create_education_dto.dict())
    education = Education.create_from(
        props=education_props, profile_id=current_user_profile_props.id
    )
    await education_repo.create_education(education.props)
    if education_props.is_current:
        user_profile = UserProfile(current_user_profile_props)
        user_profile.update_education(education.props)
        event = UserProfileUpdated.from_entity(user_profile.props)
        await event_client.publish(topic_name=settings.SNS.PROFILE_UPDATED, data=event)
    return education.props
