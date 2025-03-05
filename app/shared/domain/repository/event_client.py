from abc import ABCMeta, abstractmethod
from typing import Callable

from app.shared.domain.event.domain_event import DomainEvent


class EventClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def publish(self, topic_name: str, data: DomainEvent) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def listen(
        self,
        queue_name: str,
        callback: Callable[[str], None],
    ) -> None:
        raise NotImplementedError("Subclass should implement this")
