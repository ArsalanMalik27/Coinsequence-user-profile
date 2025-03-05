from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import AnyUrl, BaseModel

from app.domain.student.data.address import AddressProps
from app.shared.domain.data.entity import Entity


class CreateEducationProps(BaseModel):
    institution_id: UUID
    institution: str
    start_date: date | None
    end_date: date | None
    website: AnyUrl | None
    is_current: bool | None
    school_city: str | None
    school_state: str | None

    class Config:
        allow_mutation = True


class EducationProps(CreateEducationProps, Entity):
    profile_id: UUID
    address_id: UUID | None
    address: AddressProps | None

    class Config:
        allow_mutation = False
        orm_mode = True


@dataclass
class Education:
    props: EducationProps

    @staticmethod
    def create_from(props: CreateEducationProps, profile_id: UUID) -> Education:
        education_props = EducationProps(
            id=uuid4(),
            profile_id=profile_id,
            institution_id=props.institution_id,
            institution=props.institution,
            website=props.website,
            is_current=props.is_current,
            start_date=props.start_date,
            end_date=None if props.is_current else props.end_date,
            updated_at=datetime.now(),
            created_at=datetime.now(),
            school_city=props.school_city,
            school_state=props.school_state,
        )
        return Education(props=education_props)

    def update_from(self, props: CreateEducationProps) -> Education:
        education_props = EducationProps(
            **dict(
                self.props.dict(),
                institution_id=props.institution_id,
                institution=props.institution,
                start_date=props.start_date,
                end_date=None if props.is_current else props.end_date,
                is_current=props.is_current,
                website=props.website,
                updated_at=datetime.now(),
                school_city=props.school_city,
                school_state=props.school_state,
            )
        )
        self.props = education_props
