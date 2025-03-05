from dataclasses import dataclass
from datetime import datetime, date
from uuid import UUID, uuid4

from pydantic import AnyUrl, BaseModel
from typing import List, Optional

from app.domain.student.data.address import AddressProps
from app.shared.domain.data.entity import Entity


class CreateVoluntaryProps(BaseModel):
    title: str
    description: Optional[str]
    hours: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]

    class Config:
        allow_mutation = True
        orm_mode = True

class VoluntaryProps(CreateVoluntaryProps, Entity):
    profile_id: UUID

    class Config:
        allow_mutation = False
        orm_mode = True

@dataclass
class Voluntary:
    props: VoluntaryProps

    @staticmethod
    def create_from(props: CreateVoluntaryProps, profile_id: UUID):
        voluntary_props = VoluntaryProps(
            id=uuid4(),
            profile_id=profile_id,
            title=props.title,
            description=props.description,
            hours=props.hours,
            start_date=props.start_date,
            end_date=props.end_date,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        return Voluntary(props=voluntary_props)

    def update_from(self, props: CreateVoluntaryProps):
        voluntary_props = VoluntaryProps(
            **dict(
                self.props.dict(),
                title=props.title,
                description=props.description,
                hours=props.hours,
                start_date=props.start_date,
                end_date=props.end_date,
                updated_at=datetime.now(),
            )
        )
        self.props = voluntary_props