import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from app.domain.student.data.activity import ActivityType
from sqlalchemy.orm import mapped_column


class Activity(Base, BaseTableMixin):
    profile_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    activity_name = mapped_column(sq.String(255), nullable=True)
    activity_id = mapped_column(UUID(as_uuid=True))
    activity_type = mapped_column(sq.Enum(ActivityType))