import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.shared.repository.db.schema.base import Base, BaseTableMixin


class StudentFundCourses(Base, BaseTableMixin):
    user_id = mapped_column(UUID(as_uuid=True))
    college_id = mapped_column(UUID(as_uuid=True))
    course_id = mapped_column(UUID(as_uuid=True))
    college_name = mapped_column(sq.String(256))
    course_name = mapped_column(sq.String(256))
