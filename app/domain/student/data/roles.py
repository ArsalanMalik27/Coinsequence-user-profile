from enum import Enum
from dataclasses import dataclass
from datetime import datetime, date
from uuid import UUID, uuid4

from pydantic import AnyUrl, BaseModel
from typing import List, Optional

from app.domain.student.data.address import AddressProps
from app.domain.student.data.award import GradeType
from app.shared.domain.data.entity import Entity


class ParticipationTimeType(Enum):
    DURING_SCHOOL_YEAR = "DURING SCHOOL YEAR"
    DURING_SCHOOL_BREAK = "DURING SCHOOL BREAK"
    ALL_YEAR = "ALL YEAR"


class CreateRolesProps(BaseModel):
    title: str
    description: Optional[str]
    participation_time_type: Optional[ParticipationTimeType]
    hours_spent: Optional[str]
    grade: Optional[GradeType]
    start_date: date | None
    end_date: date | None

    class Config:
        allow_mutation = True
        orm_mode = True


class RolesProps(CreateRolesProps, Entity):
    profile_id: UUID

    class Config:
        allow_mutation = False
        orm_mode = True



@dataclass
class Roles:
    props: RolesProps

    @staticmethod
    def create_from(props: CreateRolesProps, profile_id: UUID):
        roles_props = RolesProps(
            id=uuid4(),
            profile_id=profile_id,
            title=props.title,
            grade=props.grade,
            description=props.description,
            hours_spent=props.hours_spent,
            participation_time_type=props.participation_time_type,
            start_date=props.start_date,
            end_date=props.end_date,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        return Roles(props=roles_props)

    def update_from(self, props: CreateRolesProps):
        roles_props = RolesProps(
            **dict(
                self.props.dict(),
                title=props.title,
                grade=props.grade,
                description=props.description,
                hours_spent=props.hours_spent,
                participation_time_type=props.participation_time_type,
                start_date=props.start_date,
                end_date=props.end_date,
                updated_at=datetime.now(),
            )
        )
        self.props = roles_props