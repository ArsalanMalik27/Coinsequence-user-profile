from enum import Enum

from app.shared.domain.data.entity import Entity

from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID, uuid4


class ActivityType(Enum):
    ACADEMIC = "ACADEMIC"
    EXTRA_CURRICULAR = "EXTRA CURRICULAR"


class CreateActivityProps(BaseModel):
    activity_name: str
    activity_id: UUID
    activity_type: ActivityType

    class Config:
        allow_mutation = True

class ActivityProps(CreateActivityProps, Entity):
    profile_id: UUID

    class Config:
        allow_mutation = False
        orm_mode = True

@dataclass
class Activity:
    props: ActivityProps

    @staticmethod
    def create_from(props: CreateActivityProps, profile_id: UUID):
        activity_props = ActivityProps(
            id=uuid4(),
            activity_name=props.activity_name,
            activity_id=props.activity_id,
            activity_type=props.activity_type,
            profile_id=profile_id,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        return Activity(props=activity_props)

    def update_from(self, props: CreateActivityProps):
        activity_props = ActivityProps(
            **dict(
                self.props.dict(),
                activity_name=props.activity_name,
                activity_id=props.activity_id,
                activity_type=props.activity_type,
                updated_at=datetime.now(),
            )
        )
        self.props = activity_props

    def delete_activity(self):
        activity_props = ActivityProps(
            **dict(
                self.props.dict(),
                deleted=True,
                updated_at=datetime.now(),
            )
        )
        self.props = activity_props