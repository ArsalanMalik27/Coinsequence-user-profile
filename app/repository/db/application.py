from typing import Any, Type
from uuid import UUID

from app.shared.repository.db.base import BaseDBRepository
from app.domain.student.repository.db.application import ApplicationRepository
from app.domain.student.data.application import ApplicationProps
from app.repository.db.schema.application import Application

class ApplicationDBRepository(
    BaseDBRepository[ApplicationProps, Application], ApplicationRepository
):
    @property
    def _table(self) -> Type[Application]:
        return Application

    @property
    def _entity(self) -> Type[ApplicationProps]:
        return ApplicationProps


    async def filter_by_profile_id(self, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = self.select().where(self._table.profile_id == profile_id)
            result = await session.execute(query)
            return list(
                map(lambda obj: self._entity.from_orm(obj), result.scalars().all())
            )