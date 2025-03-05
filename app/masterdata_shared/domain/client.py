from abc import ABCMeta, abstractmethod
from uuid import UUID
from .data import TestProps


class MasterdataClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_test(self, test_id: UUID) -> TestProps:
        raise NotImplementedError("Subclass should implement this")
