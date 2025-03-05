from typing import List, Optional, Type
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.orm import contains_eager

from app.domain.student.data.test import CreateTestProps, TestProps
from app.domain.student.repository.db.test import TestRepository
from app.repository.db.schema.score import Score
from app.repository.db.schema.test import Test
from app.shared.repository.db.base import BaseDBRepository


class TestDBRepository(BaseDBRepository[CreateTestProps, Test], TestRepository):
    @property
    def _table(self) -> Type[Test]:
        return Test

    @property
    def _entity(self) -> Type[TestProps]:
        return TestProps

    async def update_test(self, entity: TestProps) -> None:
        async with self._db_session() as session:
            entity_dict = entity.dict(exclude={"scores"})
            query = (
                update(self._table)  # type: ignore
                .where(self._table.id == entity.id)
                .values(**entity_dict)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()

    async def get_by_test_id(self, id: UUID) -> Optional[TestProps]:
        async with self._db_session() as session:
            query = (
                self.select()
                .outerjoin(Score, Score.test_id == self._table.test_id)
                .where(self._table.id == id)
                .options(contains_eager(Test.scores))
            )
            result = await session.execute(query)
            obj = result.scalars().first()
            if not obj:
                return None
            return self._entity.from_orm(obj)

    async def get_test_list_by_profile_id(self, profile_id: UUID) -> List:
        async with self._db_session() as session:
            query = (
                self.select()
                .outerjoin(
                    Score, ((Score.test_id == self._table.id) & (Score.deleted != True))
                )
                .where(self._table.profile_id == profile_id)
                .options(contains_eager(Test.scores))
            )
            result = await session.execute(query)
            return list(
                map(
                    lambda obj: self._entity.from_orm(obj),
                    result.scalars().unique().all(),
                )
            )

    async def create_test(self, entity: TestProps) -> None:
        async with self._db_session() as session:
            query = self._table(**entity.dict(exclude={"scores"}))  # type: ignore
            session.add(query)
            await session.commit()
