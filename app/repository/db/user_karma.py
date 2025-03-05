from typing import Type
from uuid import UUID

from sqlalchemy import update

from app.domain.student.data.user_karma import UserKarmaProps
from app.domain.student.repository.db.user_karma import UserKarmaRepository
from app.repository.db.schema.user_karma import UserKarma
from app.shared.repository.db.base import BaseDBRepository


class UserKarmaDBRepository(BaseDBRepository[UserKarmaProps, UserKarma], UserKarmaRepository):
    @property
    def _table(self) -> Type[UserKarma]:
        return UserKarma

    @property
    def _entity(self) -> Type[UserKarmaProps]:
        return UserKarmaProps

    async def get_by_user_id(self, user_id: UUID) -> None:
        async with self._db_session() as session:
            query = (
                self.select()
                .where(self._table.user_id == user_id)
            )
            results = await session.execute(query)
            return list(
                map(lambda obj: self._entity.from_orm(obj), results.scalars().all())
            )

    async def get_by_tag_id_and_user_id(self, user_id: UUID, tag_id: UUID) -> UserKarmaProps | None:
        async with self._db_session() as session:
            query = self.select().where(self._table.user_id == user_id, self._table.tag_id == tag_id)
            results = await session.execute(query)
            record = results.scalars().one_or_none()
            if not record:
                return None
            return self._entity.from_orm(record)

    async def create_user_karma(self, entity: UserKarmaProps) -> None:
        async with self._db_session() as session:
            query = self._table(**entity.dict())
            session.add(query)
            await session.commit()

    async def update_user_karma(self, entity: UserKarmaProps) -> None:
        async with self._db_session() as session:
            entity_dict = entity.dict()
            query = (
                update(self._table) 
                .where(self._table.id == entity.id)
                .values(**entity_dict)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount