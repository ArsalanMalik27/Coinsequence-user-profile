from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.student.event.karma_coins_minted import UserKarma as UserKarmaEvent
from app.shared.domain.data.entity import Entity


class UserKarmaProps(Entity):
    user_id: UUID
    tag_id: UUID
    name: str | None
    karma_posts: int | None
    karma_duration: int | None

    class Config:
        allow_mutation = True
        orm_mode = True


@dataclass
class UserKarma:
    props: UserKarmaProps

    @staticmethod
    def from_event(user_id: UUID, user_karma: UserKarmaEvent):
        time_now = datetime.now()
        user_profile_props = UserKarmaProps(
            id=uuid4(),
            created_at=time_now,
            updated_at=time_now,
            user_id=user_id,
            tag_id=user_karma.tag_id,
            name=user_karma.name,
            karma_posts=user_karma.karma_posts,
            karma_duration=user_karma.karma_duration,
        )
        return UserKarma(props=user_profile_props)

    def update_from_event(self, user_karma: UserKarmaEvent):
        user_profile_props = UserKarmaProps(
            **dict(
                self.props.dict(),
                karma_posts=user_karma.karma_posts,
                karma_duration=user_karma.karma_duration,
            )
        )
        self.props = user_profile_props

