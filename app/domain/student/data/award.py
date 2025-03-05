from enum import Enum

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import AnyUrl, BaseModel

from app.shared.domain.data.entity import Entity

class RecognitionType(Enum):
    SCHOOL = "SCHOOL"
    STATE = "STATE"
    NATIONAL = "NATIONAL"
    INTERNATIONAL = "INTERNATIONAL"

class GradeType(Enum):
    ONE = "1"
    TWO = "2"
    THREE  = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    ELEVEN = "11"
    TWELVE = "12"

class CreateAwardProps(BaseModel):
    title: str
    grade: GradeType
    recognition_type: RecognitionType
    description: str

    class Config:
        allow_mutation = True


class AwardProps(CreateAwardProps, Entity):
    profile_id: UUID

    class Config:
        allow_mutation = False
        orm_mode = True



@dataclass
class Award:
    props: AwardProps

    @staticmethod
    def create_from(props: CreateAwardProps, profile_id: UUID):
        award_props = AwardProps(
            id=uuid4(),
            title=props.title,
            grade=props.grade,
            recognition_type=props.recognition_type,
            description=props.description,
            profile_id=profile_id,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        return Award(props=award_props)

    def update_from(self, props: CreateAwardProps):
        award_props = AwardProps(
            **dict(
                self.props.dict(),
                title=props.title,
                grade=props.grade,
                recognition_type=props.recognition_type,
                description=props.description,
                updated_at=datetime.now(),
            )
        )
        self.props = award_props
