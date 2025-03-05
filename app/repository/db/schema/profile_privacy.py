import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID

from app.domain.student.data.profile_privacy import PrivacyType, ProfileSectionType
from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class ProfilePrivacy(Base, BaseTableMixin):
    profile_id = mapped_column(UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE"))
    profile_section_type = mapped_column(sq.Enum(ProfileSectionType))
    privacy_type = mapped_column(sq.Enum(PrivacyType))
