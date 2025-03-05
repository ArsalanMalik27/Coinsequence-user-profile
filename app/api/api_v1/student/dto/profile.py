from __future__ import annotations

from functools import reduce
from typing import Dict
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel
from app.shared.domain.data.page import PageRequestDTO,Page

from app.domain.connections.data.connection import ConnectionProps
from app.domain.connections.data.connection_request import ConnectionRequestProps
from app.domain.student.data.profile import (
    ProfileProps,
    UserProfileProps,
    UserProfileType,
)
from app.domain.student.data.profile_privacy import PrivacyType, ProfilePrivacyProps
from app.shared.domain.data.page import PageRequestDTO


class CreateUserProfileDTO(BaseModel):
    profile_type: UserProfileType


class UpdateUserProfileDTO(ProfileProps):
    pass


class UserProfileResponseDTO(UserProfileProps):
    profile_privacy: Dict | None
    pending_connection_request: int | None

    @staticmethod
    def from_props(
        profile_props: UserProfileProps,
        profile_privacies_props: ProfilePrivacyProps,
        pending_connection_request_count: int,
    ) -> UserProfileResponseDTO:
        obj = profile_props.dict()
        profile_privacy_dict = reduce(lambda aggr, new: aggr.update({new.profile_section_type.value: new.privacy_type.value}) or aggr, profile_privacies_props, {})
        obj.update(**profile_props.dict())
        obj.update({ "profile_privacy": profile_privacy_dict })
        obj.update({ "pending_connection_request" : pending_connection_request_count })
        return UserProfileResponseDTO(**obj)


class SuggestedUsersParams(PageRequestDTO):
    is_connected: bool = True
    query: str = Query(default="", title="query")

class UpdateProfilePrivacyDTO(BaseModel):
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
    children: PrivacyType

class OtherUserProfileResponseDTO(UserProfileProps):
    profile_privacy: Dict
    connection_request : ConnectionRequestProps | None
    connection_id: UUID | None
    mutual_connection_count: int | None

    @staticmethod
    def from_props(
        profile_props: UserProfileProps,
        profile_privacies_props: ProfilePrivacyProps,
        connection_request_props: ConnectionRequestProps,
        connection_props: ConnectionProps,
        mutual_counts: int,
    ) -> OtherUserProfileResponseDTO:
        obj = profile_props.dict()
        profile_privacy_dict = reduce(lambda aggr, new: aggr.update({new.profile_section_type.value: new.privacy_type.value}) or aggr, profile_privacies_props, {})
        obj.update(**profile_props.dict())
        obj.update({ "profile_privacy": profile_privacy_dict })
        obj.update({ "connection_request": connection_request_props and connection_request_props.dict() })
        obj.update({ "connection_id": connection_props and connection_props.id })
        obj.update({"mutual_connection_count": mutual_counts})
        return OtherUserProfileResponseDTO(**obj)

class ValidateParentCodeDTO(BaseModel):
    parent_code: str | None

class UserProfileListResponseDTO(Page[UserProfileProps]):
    items: list[UserProfileProps]