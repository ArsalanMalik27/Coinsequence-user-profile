import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class Test(Base, BaseTableMixin):
    test_name = mapped_column(sq.String(255))
    profile_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    test_id = mapped_column(UUID(as_uuid=True))
    # relationships
    scores = relationship("Score", backref="test")