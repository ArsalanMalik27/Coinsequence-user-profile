from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.shared.domain.data.entity import Entity
from app.shared.utils.auth import AuthUser


class ProfileSectionType(Enum):
    PERSONAL = "PERSONAL"
    EDUCATION = "EDUCATION"
    SCORE = "SCORE"
    GRADE = "GRADE"
    AWARD = "AWARD"
    COLLEGE = "COLLEGE"
    LEADERSHIP = "LEADERSHIP"
    VOLUNTARY_WORK = "VOLUNTARY_WORK"
    INTERNSHIP = "INTERNSHIP"
    ACTIVITY = "ACTIVITY"
    CHILDREN = "CHILDREN"


class PrivacyType(Enum):
    PRIVATE = "PRIVATE"
    CONNECTION = "CONNECTION"
    PUBLIC = "PUBLIC"

class ProfilePrivacyProps(Entity):
    profile_id: UUID
    profile_section_type: ProfileSectionType
    privacy_type: PrivacyType

    class Config:
        allow_mutation = True
        orm_mode = True



@dataclass
class ProfilePrivacy:
    props: ProfilePrivacyProps

    @staticmethod
    def from_user(id: uuid4, privacy_type: PrivacyType, profile_section_type: ProfileSectionType):
        time_now = datetime.now()
        profile_privacy_props = ProfilePrivacyProps(
            id=uuid4(),
            profile_id=id,
            profile_section_type=profile_section_type,
            privacy_type=privacy_type,
            created_at=time_now,
            updated_at=time_now,
        )

        return ProfilePrivacy(props=profile_privacy_props)

    def update_profile_privacy(self, profile_section_type: ProfileSectionType, privacy_type: PrivacyType):
        time_now = datetime.now()
        profile_privacy_props = ProfilePrivacyProps(
            **dict(
                self.props.dict(),
                privacy_type=privacy_type,
                profile_section_type=profile_section_type,
                updated_at=time_now,
            )
        )
        self.props = profile_privacy_props
