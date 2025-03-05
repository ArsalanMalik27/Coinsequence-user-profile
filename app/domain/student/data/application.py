from app.shared.domain.data.entity import Entity

from dataclasses import dataclass
from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime

class CreateApplicationProps(BaseModel):
    college_course_id: UUID
    course_name: str
    course_fees: int
    course_duration: int

    college_id: UUID
    college_name: str
    college_city: str
    college_state: str

    preference: int
    reason: str
    required_funds: int
    admission_status: str

    class Config:
        allow_mutation = True
        orm_mode = True

class ApplicationProps(CreateApplicationProps, Entity):
    profile_id: UUID

    class Config:
        allow_mutation = False
        orm_mode = True

@dataclass
class Application:
    props: ApplicationProps

    @staticmethod
    def create_from(props: CreateApplicationProps, profile_id: UUID):
        application_props = ApplicationProps(
            id =uuid4(),
            profile_id = profile_id,

            college_course_id = props.college_course_id,
            course_name = props.course_name,
            course_fees = props.course_fees,
            course_duration = props.course_duration,

            college_id = props.college_id,
            college_name = props.college_name,
            college_city = props.college_city,
            college_state = props.college_state,

            preference = props.preference,
            reason = props.reason,
            required_funds = props.required_funds,
            admission_status = props.admission_status,
            updated_at = datetime.now(),
            created_at = datetime.now(),
        )
        return Application(props = application_props)