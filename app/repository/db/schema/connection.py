import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class ConnectionConnection(Base, BaseTableMixin):
    user_a = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    user_b = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    is_parent = mapped_column(sq.Boolean, default=False)

    # relationship
    user_a_profile = relationship("UserProfile", foreign_keys=[user_a], lazy='noload')
    user_b_profile = relationship("UserProfile", foreign_keys=[user_b], lazy='noload')
