from abc import ABCMeta, abstractmethod
from typing import Any
from uuid import UUID


class EmailClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def add_user(
        self,
        id: UUID,
        email: str,
        first_name: str,
        last_name: str,
        token: str,
    ) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def update_tags(
        self,
        id: UUID,
        tags: dict[str, Any],
    ) -> None:
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    async def send_mail(
        self, to: str, external_user_id: UUID, template_id: str
    ) -> None:
        raise NotImplementedError("Subclass should implement this")
