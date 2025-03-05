from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class Application(BaseTableMixin, Base):
    profile_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    college_course_id = mapped_column(UUID(as_uuid=True))
    course_name = mapped_column(String)
    course_fees = mapped_column(Integer)
    course_duration = mapped_column(Integer)

    college_id = mapped_column(UUID(as_uuid=True))
    college_name = mapped_column(String)
    college_city = mapped_column(String)
    college_state = mapped_column(String)

    preference = mapped_column(Integer)
    reason = mapped_column(String)
    required_funds = mapped_column(Integer)
    admission_status = mapped_column(String)
