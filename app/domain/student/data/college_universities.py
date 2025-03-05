from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from app.shared.domain.data.entity import Entity
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID, uuid4


class UniversityProps(BaseModel):
    degree: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    university_name: Optional[str]
    university_id: Optional[UUID]

    class Config:
        allow_mutation = False
        orm_mode = True


class CreateUniversityProps(UniversityProps, Entity):
    profile_id:  UUID


@dataclass
class University:
    props: CreateUniversityProps

    @staticmethod
    def create_from(props: UniversityProps, profile_id: UUID):
        time_now = datetime.now()
        university_props = CreateUniversityProps(
            id=uuid4(),
            profile_id=profile_id,
            degree=props.degree,
            start_date=props.start_date,
            end_date=props.end_date,
            updated_at=time_now,
            created_at=time_now,
            university_name=props.university_name,
            university_id=props.university_id
        )
        print(university_props)
        return University(props=university_props)

    def update_from(self, props: UniversityProps) -> University:
        time_now = datetime.now()
        university_props = CreateUniversityProps(
            **dict(
                self.props.dict(),
                degree=props.degree,
                start_date=props.start_date,
                end_date=props.end_date,
                updated_at=time_now,
                university_name=props.university_name,
                university_id=props.university_id
            )
        )
        self.props = university_props