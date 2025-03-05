from uuid import UUID, uuid4
from dataclasses import dataclass

from app.domain.student.data.profile import UserProfileProps
from app.shared.domain.data.entity import Entity
from datetime import datetime


class ChildrenProfileProps(Entity):
    child_id: UUID
    parent_id: UUID
    is_confirmed: bool | None


    class Config:
        allow_mutation = False
        orm_mode = True


@dataclass
class Children_Profile:
    props: ChildrenProfileProps

    @staticmethod
    def from_users(child_id: UUID, parent_id: UUID):
        time_now = datetime.now()
        child_profile_props = ChildrenProfileProps(
            id=uuid4(),
            child_id=child_id,
            parent_id=parent_id,
            is_confirmed=False,
            created_at=time_now,
            updated_at=time_now,
        )
        return Children_Profile(props=child_profile_props)

    def update_confirmation(self):
        child_profile_props = ChildrenProfileProps(**dict(
            self.props.dict(),
            is_confirmed=True,
            updated_at=datetime.now(),
        ))
        return Children_Profile(props=child_profile_props)
