from typing import Optional, Type
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.future import select

from app.domain.student.data.profile_privacy import (
    ProfilePrivacyProps,
    ProfileSectionType,
)
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.repository.db.schema.profile_privacy import ProfilePrivacy
from app.shared.repository.db.base import BaseDBRepository


class ProfilePrivacyDBRepository(
    BaseDBRepository[ProfilePrivacyProps, ProfilePrivacy], ProfilePrivacyRepository
):
    @property
    def _table(self) -> Type[ProfilePrivacy]:
        return ProfilePrivacy

    @property
    def _entity(self) -> Type[ProfilePrivacyProps]:
        return ProfilePrivacyProps

    async def filter(self, profile_id: UUID) -> list[ProfilePrivacyProps]:
        async with self._db_session() as session:
            query = self.select().where(ProfilePrivacy.profile_id == profile_id)
            results = await session.execute(query)
            return list(
                map(lambda obj: self._entity.from_orm(obj), results.scalars().all())
            )

    async def get_profile_privacy_by_section(
        self, profile_id: UUID, profile_section_type: ProfileSectionType
    ) -> Optional[ProfilePrivacyProps]:
        async with self._db_session() as session:
            query = select(self._table).where(
                and_(
                    ProfilePrivacy.profile_id == profile_id,
                    ProfilePrivacy.profile_section_type == profile_section_type,
                )
            )
            result = await session.execute(query)
            obj = result.scalars().first()
            if not obj:
                return None
            return self._entity.from_orm(obj)
