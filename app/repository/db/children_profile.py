from typing import Type
from uuid import UUID

from sqlalchemy import and_, func

from app.domain.student.data.children_profile import ChildrenProfileProps
from app.domain.student.data.profile import UserProfile
from app.domain.student.repository.db.children_profile import ChildrenProfileRepository
from app.repository.db.schema.children_profile import ChildrenProfile
from app.repository.db.schema.profile import UserProfile
from app.shared.repository.db.base import BaseDBRepository


class ChildrenProfileDBRepository(
    BaseDBRepository[ChildrenProfileProps, ChildrenProfile], ChildrenProfileRepository
):
    @property
    def _table(self) -> Type[ChildrenProfile]:
        return ChildrenProfile

    @property
    def _entity(self) -> Type[ChildrenProfileProps]:
        return ChildrenProfileProps

    async def filter_by_parent_id(self, parent_id: UUID) -> list[ChildrenProfileProps]:
        async with self._db_session() as session:
            query = self.select().where(
                and_(
                    ChildrenProfile.parent_id == parent_id,
                    ChildrenProfile.is_confirmed == True,
                )
            )
            result = await session.execute(query)
            return list(
                map(lambda obj: self._entity.from_orm(obj), result.scalars().all())
            )

    async def count_children_by_child_id(self, child_id: UUID) -> int:
        async with self._db_session() as session:
            query = self.select().where(self._table.child_id == child_id)
            counter = query.with_only_columns(func.count())
            results = await session.execute(counter)
            count = results.scalar()
            return count

    async def get_by_profile_ids(
        self, child_id: UUID, parent_id: UUID
    ) -> ChildrenProfileProps:
        async with self._db_session() as session:
            query = self.select().where(
                and_(
                    ChildrenProfile.parent_id == parent_id,
                    ChildrenProfile.child_id == child_id,
                )
            )
            result = await session.execute(query)
            obj = result.scalars().first()
            if not obj:
                return None
            return self._entity.from_orm(obj)
