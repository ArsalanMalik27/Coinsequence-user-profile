import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.shared.repository.db.schema.base import Base, BaseTableMixin


class UserKarma(Base, BaseTableMixin):
    user_id = mapped_column(UUID(as_uuid=True), nullable=False)
    tag_id = mapped_column(UUID(as_uuid=True))
    name = mapped_column(sq.String(1024), nullable=True)
    karma_posts = mapped_column(sq.Integer)
    karma_duration = mapped_column(sq.Integer)