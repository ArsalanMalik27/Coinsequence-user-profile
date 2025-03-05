from abc import ABCMeta, abstractmethod
from uuid import UUID

from app.domain.student.data.profile import UserProfileProps

USER_CONNECTIONS_FEED = "user_connections"
TIMELINE_FEED = "timeline"


class ActivityStream:
    __metaclass__ = ABCMeta

    @abstractmethod
    def follow(self, follower_id: str, follow_id: str) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    def unfollow(self, follower_id: str, follow_id: str) -> None:
        raise NotImplementedError("Subclass should implement this")
