from typing import Any

import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from app.domain.student.data.gender import Gender
from app.domain.student.data.profile import UserProfileType
from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class ChildrenProfile(Base, BaseTableMixin):
    child_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    parent_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    is_confirmed = mapped_column(sq.Boolean, default=False)


