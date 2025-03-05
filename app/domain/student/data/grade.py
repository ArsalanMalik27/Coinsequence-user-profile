from __future__ import annotations
from uuid import uuid4, UUID
from datetime import datetime
from dataclasses import dataclass

from pydantic import BaseModel

from app.shared.domain.data.entity import Entity

from typing import List, Optional


class CreateGradeProps(BaseModel):
    level: str
    gpa: str
    courses: Optional[List[str]]
    institution: Optional[str]
    institution_id: Optional[UUID]
    max_gpa: Optional[str]

    class Config:
        allow_mutation = True


class GradeProps(CreateGradeProps, Entity):
    profile_id: UUID

    class Config:
        allow_mutation = False
        orm_mode = True


@dataclass
class Grade:
    props: GradeProps

    @staticmethod
    def create_from(props: CreateGradeProps, profile_id: UUID) -> Grade:
        grade_props = GradeProps(
            id=uuid4(),
            level=props.level,
            gpa=props.gpa,
            courses=props.courses,
            updated_at=datetime.now(),
            created_at=datetime.now(),
            profile_id=profile_id,
            institution=props.institution,
            institution_id=props.institution_id,
            max_gpa=props.max_gpa
        )
        return Grade(props=grade_props)

    def update_from(self, props: CreateGradeProps) -> Grade:
        grade_props = GradeProps(
            **dict(
                self.props.dict(),
                level=props.level,
                gpa=props.gpa,
                courses=props.courses,
                institution=props.institution,
                institution_id=props.institution_id,
                updated_at=datetime.now(),
                max_gpa=props.max_gpa
            )
        )
        self.props = grade_props
