from enum import Enum

from dataclasses import dataclass
from datetime import datetime, date
from uuid import UUID, uuid4

from pydantic import AnyUrl, BaseModel

from app.shared.domain.data.entity import Entity



class WorkType(Enum):
    PAID_INTERNSHIP = "INTERNSHIP (PAID)"
    UNPAID_INTERNSHIP = "INTERNSHIP (UNPAID)"
    PAID_WORK = "PAID WORK"

class CreateWorkProps(BaseModel):
    title: str
    description: str
    work_type: WorkType
    net_hours: str
    start_date: date
    end_date: date

    class Config:
        allow_mutation = True


class WorkProps(CreateWorkProps, Entity):
    profile_id: UUID

    class Config:
        allow_mutation = False
        orm_mode = True

@dataclass
class Work:
    props: WorkProps

    @staticmethod
    def create_from(props: CreateWorkProps, profile_id: UUID):
        work_props = WorkProps(
            id=uuid4(),
            title=props.title,
            description=props.description,
            work_type=props.work_type,
            profile_id=profile_id,
            net_hours=props.net_hours,
            start_date=props.start_date,
            end_date=props.end_date,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        return Work(props=work_props)

    def update_from(self, props: CreateWorkProps):
        work_props = WorkProps(
            **dict(
                self.props.dict(),
                title=props.title,
                description=props.description,
                work_type=props.work_type,
                net_hours=props.net_hours,
                start_date=props.start_date,
                end_date=props.end_date,
                updated_at=datetime.now(),
            )
        )
        self.props = work_props
