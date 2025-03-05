import stream

from app.domain.connections.repository.activity_stream import (
    TIMELINE_FEED,
    USER_CONNECTIONS_FEED,
    ActivityStream,
)
from app.infra.config import settings


class GetStreamActivityStream(ActivityStream):
    def __init__(self) -> None:
        self._getstream_client = stream.connect(
            settings.GETSTREAM_API_KEY, settings.GETSTREAM_SECRET
        )

    def follow(self, follower_id: str, follow_id: str) -> None:
        timeline_feed = self._getstream_client.feed(TIMELINE_FEED, str(follower_id))
        timeline_feed.follow(USER_CONNECTIONS_FEED, follow_id)

    def unfollow(self, follower_id: str, follow_id: str) -> None:
        timeline_feed = self._getstream_client.feed(TIMELINE_FEED, str(follower_id))
        timeline_feed.unfollow(USER_CONNECTIONS_FEED, follow_id)
