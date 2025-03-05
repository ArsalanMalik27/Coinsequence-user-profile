from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.student.data.profile import UserProfileProps
from app.shared.domain.data.entity import Entity


class ConnectionProps(Entity):
    user_a: UUID
    user_b: UUID
    user_a_profile: UserProfileProps | None
    user_b_profile: UserProfileProps | None
    is_parent: bool | None

    class Config:
        allow_mutation = False
        orm_mode = True


@dataclass
class Connection:
    props: ConnectionProps

    @staticmethod
    def from_users(user_a: UUID, user_b: UUID, is_parent: bool) -> Connection:
        time_now = datetime.now()
        user_profile_props = ConnectionProps(
            id=uuid4(),
            user_a=user_a,
            user_b=user_b,
            created_at=time_now,
            updated_at=time_now,
            is_parent=is_parent,
        )
        return Connection(props=user_profile_props)
