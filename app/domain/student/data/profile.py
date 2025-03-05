from __future__ import annotations

import math
import random
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import AnyUrl, BaseModel

from app.domain.student.data.education import EducationProps
from app.domain.student.data.gender import Gender
from app.domain.student.data.profile_privacy import PrivacyType
from app.shared.domain.data.entity import Entity
from app.shared.repository.storage_client import FileInfo
from app.shared.utils.auth import AuthUser


def generate_parent_code() -> str:
    digits = "0123456789"
    parent_code = ""
    for i in range(6):
        parent_code += digits[math.floor(random.random() * 10)]
    return parent_code


class UserProfileType(Enum):
    STUDENT = "STUDENT"
    INVESTOR = "INVESTOR"
    TEACHER = "TEACHER"
    PARENT = "PARENT"


class ProfilePrivacyTypeProps(BaseModel):
    personal: PrivacyType
    education: PrivacyType
    score: PrivacyType
    grade: PrivacyType
    college: PrivacyType
    award: PrivacyType
    leadership: PrivacyType
    voluntary_work: PrivacyType
    internship: PrivacyType
    activity: PrivacyType


class ProfileProps(BaseModel):
    profile_type: Optional[UserProfileType]
    legal_name: Optional[str]
    pronoun: Optional[str]
    profile_image: Optional[AnyUrl]
    profile_image_thumbnail: Optional[AnyUrl]
    ethinicity: Optional[str]
    sub_ethinicity: Optional[str]
    dob: Optional[date]
    gender: Optional[Gender]
    nationality: Optional[str]
    headline: Optional[str]
    summary: Optional[str]
    hobbies: Optional[List[str]]
    connection_count: Optional[int]
    karmapost_count: Optional[int]
    karmavalidation_count: Optional[int]
    karma_time: Optional[int]
    karma_coin: Optional[int]
    ethinicity_id: Optional[UUID]
    sub_ethinicity_id: Optional[UUID]
    city: Optional[str]
    disability: Optional[str]
    family_type: Optional[str]
    socio_economic_group: Optional[str]
    disability_id: Optional[UUID]
    family_type_id: Optional[UUID]
    socio_economic_group_id: Optional[UUID]


class UserProfileProps(ProfileProps, Entity):
    first_name: Optional[str]
    last_name: Optional[str]
    user_id: UUID
    educations: list[EducationProps] | None
    parent_code: Optional[str]

    class Config:
        allow_mutation = True
        orm_mode = True

    # @staticmethod
    # def from_orm_custom(obj):
    #     current_education = obj.educations[0]
    #     entity = UserProfileProps.from_orm(obj)
    #     entity.current_education = current_education
    #     return entity


@dataclass
class UserProfile:
    props: UserProfileProps

    @staticmethod
    def from_user(user: AuthUser, profile_type: UserProfileType) -> UserProfile:
        time_now = datetime.now()
        parent_code = generate_parent_code()
        user_profile_props = UserProfileProps(
            id=uuid4(),
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            profile_type=profile_type,
            created_at=time_now,
            updated_at=time_now,
            parent_code=parent_code,
            disability='',
            family_type='',
            socio_economic_group=''

        )
        return UserProfile(props=user_profile_props)

    def update_from(self, props: UserProfileProps) -> UserProfile:
        user_profile_props = UserProfileProps(
            **dict(
                self.props.dict(),
                profile_type=props.profile_type,
                legal_name=props.legal_name,
                pronoun=props.pronoun,
                profile_image=props.profile_image,
                profile_image_thumbnail=props.profile_image_thumbnail,
                ethinicity=props.ethinicity,
                sub_ethinicity=props.sub_ethinicity,
                dob=props.dob,
                gender=props.gender,
                nationality=props.nationality,
                headline=props.headline,
                summary=props.summary,
                hobbies=props.hobbies,
                connection_count=props.connection_count,
                karmapost_count=props.karmapost_count,
                karmavalidation_count=props.karmavalidation_count,
                karma_time=props.karma_time,
                karma_coin=props.karma_coin,
                ethinicity_id=props.ethinicity_id,
                sub_ethinicity_id=props.sub_ethinicity_id,
                city=props.city,
                disability=props.disability,
                family_type=props.family_type,
                socio_economic_group=props.socio_economic_group,
                disability_id=props.disability_id,
                family_type_id=props.family_type_id,
                socio_economic_group_id=props.socio_economic_group_id,
            )
        )

        self.props = user_profile_props

    def update_name(self, first_name: str, last_name: str) -> UserProfile:
        user_profile_props = UserProfileProps(
            **dict(
                self.props.dict(),
                first_name=first_name,
                last_name=last_name,
            )
        )
        self.props = user_profile_props

    def update_profile_pic(self, fileinfo: FileInfo) -> UserProfile:
        user_profile_props = UserProfileProps(
            **dict(
                self.props.dict(),
                profile_image=fileinfo["url"],
                profile_image_thumbnail=fileinfo["url"],
            )
        )
        self.props = user_profile_props

    def update_education(self, education_props: EducationProps) -> UserProfile:
        user_profile_props = UserProfileProps(
            **dict(self.props.dict(), educations=[education_props])
        )
        self.props = user_profile_props

    def update_parent_code(self) -> UserProfile:
        parent_code = generate_parent_code()
        user_profile_props = UserProfileProps(
            **dict(
                self.props.dict(),
                parent_code=parent_code,
            )
        )
        self.props = user_profile_props

    def update_connection_count(self, connection_count) -> UserProfile:
        user_profile_props = UserProfileProps(
            **dict(
                self.props.dict(),
                connection_count=connection_count,
            )
        )
        self.props = user_profile_props

    def add_karma_coins(self, karma_coins) -> UserProfile:
        user_profile_props = UserProfileProps(
            **dict(
                self.props.dict(),
                karma_coin=self.props.karma_coin + karma_coins,
            )
        )
        self.props = user_profile_props
