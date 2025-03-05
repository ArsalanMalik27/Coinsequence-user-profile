from __future__ import annotations

from uuid import UUID

from pydantic import AnyUrl, BaseModel

from app.domain.student.data.profile import UserProfileProps, UserProfileType
from app.shared.domain.event.domain_event import DomainEvent


class UserProfileUpdatedData(BaseModel):
    id: UUID
    user_id: UUID
    first_name: str | None
    last_name: str | None
    profile_image: AnyUrl | None
    profile_image_thumbnail: AnyUrl | None
    school_name: str | None
    school_id: UUID | None
    pronoun: str | None
    school_city: str | None
    school_state: str | None
    profile_type: UserProfileType | None

    class Config:
        allow_mutation = False

class UserProfileUpdated(DomainEvent):
    name: str = "ProfileUpdated"
    data: UserProfileUpdatedData

    @classmethod
    def from_entity(cls, entity: UserProfileProps) -> UserProfileUpdated:
        data = UserProfileUpdatedData(
            id=entity.id,
            user_id=entity.user_id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            profile_type=entity.profile_type,
            profile_image=entity.profile_image,
            profile_image_thumbnail=entity.profile_image_thumbnail,
            school_name=entity.educations[0].institution if entity.educations and (len(entity.educations) > 0) else None,
            school_id=entity.educations[0].id if entity.educations and (len(entity.educations) > 0) else None,
            pronoun=entity.pronoun,
            school_city=entity.educations[0].school_city if entity.educations and (len(entity.educations) > 0) else None,
            school_state=entity.educations[0].school_state if entity.educations and (len(entity.educations) > 0) else None,
        )
        return UserProfileUpdated(data=data)
