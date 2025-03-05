from typing import Type
from uuid import UUID

from sqlalchemy import update

from app.domain.student.data.roles import RolesProps
from app.domain.student.repository.db.roles import RolesRepository
from app.repository.db.schema.roles import Roles
from app.shared.repository.db.base import BaseDBRepository


class RolesDBRepository(BaseDBRepository[RolesProps, Roles], RolesRepository):
    @property
    def _table(self) -> Type[Roles]:
        return Roles

    @property
    def _entity(self) -> Type[RolesProps]:
        return RolesProps

    async def create_roles(self, entity: RolesProps) -> None:
        async with self._db_session() as session:
            query = self._table(**entity.dict())  # type: ignore
            session.add(query)
            await session.commit()

    async def update_roles(self, entity: RolesProps, profile_id: UUID) -> None:
        async with self._db_session() as session:
            entity_dict = entity.dict()
            query = (
                update(self._table)  # type: ignore
                .where(
                    (self._table.id == entity.id)
                    & (self._table.profile_id == profile_id)
                )
                .values(**entity_dict)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def delete_roles(self, roles_id: UUID, profile_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                update(self._table)  # type: ignore
                .where(
                    (self._table.id == roles_id)
                    & (self._table.profile_id == profile_id)
                )
                .values(deleted=True)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def get_all_roles(self, profile_id) -> list[RolesProps]:
        async with self._db_session() as session:
            query = (
                self.select()
                .where(self._table.profile_id == profile_id)
                .execution_options(synchronize_session="fetch")
            )
            results = await session.execute(query)
            return list(
                map(lambda obj: self._entity.from_orm(obj), results.scalars().all())
            )
