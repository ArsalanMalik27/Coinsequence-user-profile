import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.domain.connections.data.connection_request import ConnectionRequestStatus
from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class ConnectionRequestConnection(Base, BaseTableMixin):
    sender_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    receiver_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    status = mapped_column(sq.Enum(ConnectionRequestStatus))
    is_parent = mapped_column(sq.Boolean, default=False)

    # relationship
    sender = relationship("UserProfile", foreign_keys=[sender_id])
    receiver = relationship("UserProfile", foreign_keys=[receiver_id])
