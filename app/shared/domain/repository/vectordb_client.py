from abc import ABCMeta, abstractmethod


class VectorDBClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    def upsert(self, id: str, data: str, metadata: dict):
        raise NotImplementedError("Subclass should implement this")

    @abstractmethod
    def query(self, query: str):
        raise NotImplementedError("Subclass should implement this")
