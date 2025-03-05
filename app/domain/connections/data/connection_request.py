from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.domain.student.data.profile import UserProfileProps
from app.shared.domain.data.entity import Entity


class ConnectionRequestStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class CreateConnectionRequestProps(BaseModel):
    receiver_id: UUID

    class Config:
        allow_mutation = False


class ConnectionRequestProps(CreateConnectionRequestProps, Entity):
    status: ConnectionRequestStatus
    sender_id: UUID
    sender: UserProfileProps | None
    receiver: UserProfileProps | None
    is_parent: bool | None


    class Config:
        allow_mutation = False
        orm_mode = True


@dataclass
class ConnectionRequest:
    props: ConnectionRequestProps

    @staticmethod
    def from_create_props(props: CreateConnectionRequestProps, sender_id: UUID) -> ConnectionRequest:
        time_now = datetime.now()
        connection_request_props = ConnectionRequestProps(
            id=uuid4(),
            sender_id=sender_id,
            receiver_id=props.receiver_id,
            created_at=time_now,
            updated_at=time_now,
            status=ConnectionRequestStatus.PENDING,
            is_parent=False,
        )
        return ConnectionRequest(props=connection_request_props)

    @staticmethod
    def from_connection_request_props(
        props: ConnectionRequestProps,
    ) -> ConnectionRequest:
        return ConnectionRequest(props=props)

    def request(self) -> None:
        connection_request_props = ConnectionRequestProps(
            **dict(self.props.dict(), status=ConnectionRequestStatus.PENDING, updated_at=datetime.now())
        )
        self.props = connection_request_props

    def accept(self) -> None:
        connection_request_props = ConnectionRequestProps(
            **dict(self.props.dict(), status=ConnectionRequestStatus.ACCEPTED, updated_at=datetime.now())
        )
        self.props = connection_request_props

    def reject(self) -> None:
        connection_request_props = ConnectionRequestProps(
            **dict(self.props.dict(), status=ConnectionRequestStatus.REJECTED, updated_at=datetime.now())
        )
        self.props = connection_request_props

    def is_parent(self) -> None:
        connection_request_props = ConnectionRequestProps(
            **dict(self.props.dict(), is_parent=True)
        )
        self.props = connection_request_props