from abc import ABCMeta, abstractmethod
from typing import TypedDict
from uuid import UUID

from fastapi import UploadFile


class FileInfo(TypedDict):
    url: str
    path: str


class StorageClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def upload(
        self, folder: str, actor_id: UUID, files: list[UploadFile]
    ) -> list[FileInfo]:
        raise NotImplementedError("Subclass should implement this")
