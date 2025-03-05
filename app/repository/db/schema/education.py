import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.repository.db.schema.address import Address  # This is needed for sequence
from app.shared.repository.db.schema.base import Base, BaseTableMixin


class Education(BaseTableMixin, Base):
    profile_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    institution_id = mapped_column(UUID(as_uuid=True))
    institution = mapped_column(sq.String(255))
    start_date = mapped_column(sq.DateTime, nullable=True)
    end_date = mapped_column(sq.DateTime, nullable=True)
    is_current = mapped_column(sq.Boolean, default=False)
    website = mapped_column(sq.String(255), nullable=True)
    address_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("address.id", ondelete="CASCADE"), nullable=True
    )
    school_city = mapped_column(sq.String(256), default="")
    school_state = mapped_column(sq.String(256), default="")

    # relationship
    address = relationship("Address", foreign_keys=[address_id], lazy="joined")
